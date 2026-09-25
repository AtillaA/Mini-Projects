def quicksort(V, l, r):
    if l >= r:
        return
        
    i = l
    j = r
    p = (l+r)//2 # pivot in the middle
    x = V[p]
    
    while i<j:
        while x > V[i]:
            i+=1
            
        while V[j] > x:
            j-=1
            
        if i <= j:
            swap(V, i, j) # auxiliary procedure
            i+=1
            j-=1
            
    if l<j:
        quicksort(V, l, j)
        
    if i<r:
        quicksort(V, i, r)
        
    return V
  
