// url check throttler
function throttle<T extends (...args: any[]) => void>(func: T, limit: number): T & { cancel: () => void } {
  let isThrottled: boolean = false; // lock
  let lastArgs: any[] | null = null; // last keystrokes
  let lastContext: any = null; // latest context

  // intercept keystrokes
  const throttledFn = function(this: any, ...args: any[]) {
    if (!isThrottled) {
      func.apply(this, args);
      isThrottled = true;

      // countdown timer
      // recursive approach to cover for pending inputs
      const runTimeout = () => {
        setTimeout(() => {
          if (lastArgs) { // check for ignored inputs
            func.apply(lastContext, lastArgs);
            lastArgs = null;
            lastContext = null;
            runTimeout(); // keep the lock active and start a new cycle
          } else {
            isThrottled = false;
          } // release lock once there are no trailing calls
        }, limit);
      };
      runTimeout();
    } else { 
      lastArgs = args; 
      lastContext = this; // store context of ignored input
    } // save latest to run 
  };

  // add cancel capability to flush queued execution
  (throttledFn as any).cancel = () => {
    lastArgs = null;
    lastContext = null;
    isThrottled = false;
  };

  return throttledFn as any;
}

// main controller app
class UrlChecker {
  private urlInput: HTMLInputElement;
  private formatStatus: HTMLElement;
  private serverStatus: HTMLElement;

  // for tracking the absolute latest request
  // and to invalidate older requests
  private requestId: number = 0;
  private issuedRequestId: number = 0; // to track actual sent executions

  // handler for throttling server calls (1000 ms)
  // defined as a class property to preserve
  private throttledCheck = throttle(() => {
    const currentUrl = this.urlInput.value.trim();
  
    // strict check, abort execution entirely
    if (!currentUrl || !this.checkFormat(currentUrl)) { return; }

    this.issuedRequestId++;
    
    // format the string value for the server check
    const target = /^(https?:\/\/)/i.test(currentUrl) ? currentUrl : `https://${currentUrl}`;
    this.serverCheck(target, this.issuedRequestId); 
  }, 1000);



  constructor() {
    this.urlInput = document.getElementById('urlInput') as HTMLInputElement;
    this.formatStatus = document.getElementById('formatStatus') as HTMLElement;
    this.serverStatus = document.getElementById('serverStatus') as HTMLElement;
    this.initEventListeners();
  }

  private initEventListeners(): void {
    // listener for per keystroke
    this.urlInput.addEventListener('input', (event: Event) => {
      const target = event.target as HTMLInputElement;
      const rawUrl = target.value;
      const url = rawUrl.trim(); // ignore leading/trailing ws

      // base condition
      if (!url) {
        this.clear();
        return;
      }

      // check URL structure
      const isValid = this.checkFormat(url);
      console.log(`User typed: "${url}" | Format Valid: ${isValid}`);

      // if there are ws in the middle
      if (/\S\s+\S/.test(rawUrl)) {
        this.updateStatus(this.formatStatus, 'INVALID');
        this.updateStatus(this.serverStatus, 'Waiting...');
        return;
      } else if (isValid) {
        this.updateStatus(this.formatStatus, 'VALID');
        this.updateStatus(this.serverStatus, 'Checking...');

        this.requestId++; // increment on every keystroke
        console.log(`Request ID: ${this.requestId} | URL: ${url}`);
        
        // ensure string is passed
        //const target = /^(https?:\/\/)/i.test(url) ? url : `https://${url}`;
        this.throttledCheck();
      } else {
        this.updateStatus(this.formatStatus, 'INVALID');
        this.updateStatus(this.serverStatus, 'Waiting...');
      }
    });
  }

  // format check on client-side
  private checkFormat(url: string): boolean {
    try {
      // inject native protocol
      const parsed = new URL(/^(https?:\/\/)/i.test(url) ? url : `https://${url}`);
      
      // template regex
      const pattern = /^.+\.[a-z0-9-]{2,}$/i;
      return pattern.test(parsed.hostname);
    } catch (_) { return false; }
  }

  // async check method
  private async serverCheck(url: string, requestId: number): Promise<void> {
    try {
      console.log(`Async fetch for: "${url}"`);

      // wait for server to resolve
      const result = await MockServer.checkUrl(url);
      console.log(`Received result for: "${url}" -> Exists: ${result.exists}, Type: ${result.type}`);

      // race condition
      if (requestId !== this.issuedRequestId) {
        console.warn(`ABORTED! Stale request (current: #${requestId} | latest: #${this.issuedRequestId})`);
        return;
      }

      // check if text is altered while current request was running
      const currentUrl = this.urlInput.value.trim();
      const currentTarget = /^(https?:\/\/)/i.test(currentUrl) ? currentUrl : `https://${currentUrl}`;
      
      if (url.toLowerCase() !== currentTarget.toLowerCase() || !this.checkFormat(currentUrl)) {
        console.warn("ABORTED! Input context changed while server request was pending.");
        return;
      }

      // if URL exists, check file or folder
      if (result.exists) { this.updateStatus(this.serverStatus, `URL exists! (Type: ${result.type.toUpperCase()})`); }
      else { this.updateStatus(this.serverStatus, 'URL does not exist.'); }

      console.log(`UI updated for: "${url}"`);
    } catch (error) { this.updateStatus(this.serverStatus, 'Connection error...'); }
  }

  // UI helper
  private updateStatus(element: HTMLElement, text: string): void { 
    element.textContent = text; 
    // config mapping
    const classes: Record<string, string> = {
    'invalid': 'status-invalid',
    'error': 'status-invalid',
    'waiting': 'status-waiting',
    'checking': 'status-checking',
    'exist': 'status-valid',
    'valid': 'status-valid' 
  };

    // find matching keyword or fallback to default
    const lowerText = text.toLowerCase();
    const matchedKey = Object.keys(classes).find(key => lowerText.includes(key));
    const activeClass = matchedKey ? classes[matchedKey] : 'status-none';

    element.className = `status ${activeClass}`;
  }

  // clear status texts
  private clear(): void {
    this.requestId++;
    this.issuedRequestId++;

    this.formatStatus.textContent = '-';
    this.serverStatus.textContent = '-';
  }
}

// mock server class
class MockServer {
  public static async checkUrl(url: string): Promise<{ exists: boolean; type: 'file' | 'folder' | 'unknown' }> {
    try {
      // inject http or https if needed
      const target = /^(https?:\/\/)/i.test(url) ? url : `https://${url}`;
      new URL(target);
    } catch (_) { return { exists: false, type: 'unknown' }; } // if fails, exit early

    // superficial latency wrapper (1000ms)
    await new Promise(resolve => setTimeout(resolve, 1000));

    const mockUrl = url.toLowerCase(); // ignore capitals
    
    if (mockUrl.includes('localhost') || mockUrl.includes('local') || mockUrl.includes('.invalid')) { return { exists: false, type: 'unknown' }; }
    if (mockUrl.endsWith('/') || mockUrl.includes('/dir/')) { return { exists: true, type: 'folder' }; } // folder
    return { exists: true, type: 'file' }; // default fallback (file)
  }
}

// init app
document.addEventListener('DOMContentLoaded', () => { new UrlChecker(); });
