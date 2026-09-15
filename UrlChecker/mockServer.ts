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

export { MockServer };
