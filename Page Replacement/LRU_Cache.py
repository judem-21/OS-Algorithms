class Node:
    def __init__(self,data):
        self.data=data
        self.next=None
        self.prev=None
class LRU:
    def __init__(self,capacity):
        self.capacity=capacity
        self.size=0
        self.map={}
        self.head=Node([-1,-1])
        self.tail=Node([-1,-1])
        self.head.next=self.tail
        self.tail.prev=self.head

    def remove(self,node):
        next_node=node.next
        prev_node=node.prev
        prev_node.next=next_node
        next_node.prev=prev_node
        self.size-=1

    def get(self,key):
        if key in self.map:
            temp = self.map[key].data
            self.remove(self.map[key])
            del self.map[key]
            self.put(temp[0],temp[1])
            return temp
        return -1

    def put(self,key,value):
        if key in self.map:
            self.map[key].data=[key,value]
            newNode=self.map[key]
            self.remove(newNode)
        else:
            newNode = Node([key, value])
            self.map[key] = newNode
            if self.size == self.capacity:
                del self.map[self.tail.prev.data[0]]
                self.remove(self.tail.prev)
        tempNode = self.head.next
        if tempNode==newNode:return
        self.head.next = newNode
        newNode.next = tempNode
        newNode.prev = self.head
        tempNode.prev = newNode
        if self.size < self.capacity: self.size += 1

    def display(self):
        if self.size==0: print('Cache empty!!');return
        print('Cache currently contains:')
        curr=self.head.next
        while curr and curr.data!=[-1,-1]:
            print(curr.data,end='-->')
            curr=curr.next
        print()

if __name__=='__main__':
    lru_cache = LRU(capacity=2)
    lru_cache.put(2, 1)
    print('Cache now is: ')
    lru_cache.display()
    lru_cache.put(1, 1)
    print('Cache now is: ')
    lru_cache.display()
    lru_cache.put(2, 3)
    print('Cache now is: ')
    lru_cache.display()




