class Queue():
    def __init__(self): #Constructor and Members

        self.lst = []

    def isempty(self): 
        '''Function to check whether the queue is empty'''
        if len(self.lst) == 0:
            
            return True
        else:
            return False
        
    def enqueue(self,ele): 
        '''Adding elements at the end of the queue'''
        self.lst.append(ele)
    
    def dequeue(self):
        '''Removing elements at the front of the queue'''
        return self.lst.pop(0)

    def __len__(self):
        '''Returns length of Stack'''
        return len(self.lst)
    
    def __getitem__(self,ind):

        return self.lst[ind]
    
    def __str__(self):

        return str(self.lst)