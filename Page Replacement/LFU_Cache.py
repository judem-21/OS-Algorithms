class Node:
    def __init__(self,data):
        self.data=data
        self.next=None
        self.prev=None
        
class LFUCache:
    def __init__(self,capacity):
        self.map_freq= {}
        self.map_key = {}
        self.capacity=capacity
        self.size=0
        self.min_freq=1

    def add_to_cache(self,node,freq):
        if freq not in self.map_freq:
            tempNode_head = Node([-1, -1])
            tempNode_tail = Node([-1, -1])
            tempNode_head.next = tempNode_tail
            tempNode_tail.prev = tempNode_head
            self.map_freq[freq]=[tempNode_head, tempNode_tail,1]
        else:
            self.map_freq[freq][-1]+=1
        self.min_freq = min(self.min_freq, freq)
        tempNode=self.map_freq[freq][0].next
        self.map_freq[freq][0].next=node
        node.prev=self.map_freq[freq][0]
        node.next=tempNode
        tempNode.prev=node

    def remove_from_cache(self,node,freq):
        next_node,prev_node=node.next,node.prev
        next_node.prev=prev_node
        prev_node.next=next_node
        self.map_freq[freq][-1]=max(self.map_freq[freq][-1]-1,0)
        if freq == self.min_freq and self.map_freq[freq][-1] == 0:
            self.min_freq+=1

    def delete_key(self,key):
        if key in self.map_key:
            freq=self.map_key[key][1]
            self.remove_from_cache(self.map_key[key][0],freq)
            del self.map_key[key]
            return
        return -1

    def get(self, key):
        if key in self.map_key:
            freq=self.map_key[key][1]
            self.remove_from_cache(self.map_key[key][0],freq)
            self.add_to_cache(self.map_key[key][0],freq+1)
            self.map_key[key][1]=freq+1
            return self.map_key[key][0].data[1]
        return -1

    def put(self, key, value):
        if self.capacity == 0:
            return

        if key in self.map_key:
            freq = self.map_key[key][1]
            self.remove_from_cache(self.map_key[key][0], freq)
            self.add_to_cache(self.map_key[key][0], freq + 1)
            self.map_key[key][0].data = [key, value]
            self.map_key[key][1] = freq + 1
            return

        if self.size == self.capacity:
            delete_node = self.map_freq[self.min_freq][1].prev
            delete_key = delete_node.data[0]
            self.delete_key(delete_key)
            self.size = max(self.size-1,0)  # adjust size here

        # Insert new key
        newNode = Node([key, value])
        self.map_key[key] = [newNode, 1]
        self.add_to_cache(newNode, freq=1)
        self.min_freq = 1
        self.size = min(self.size+1,self.capacity)

    def display(self):
        if self.size == 0: print('Cache empty!!');return
        print('Cache currently contains:')
        for i in self.map_freq:
            if self.map_freq[i][-1]>0:
                print(f'Freq = {i}:')
                curr=self.map_freq[i][0].next
                while curr and curr.data!=[-1,-1]:
                    print(curr.data,end='-->')
                    curr=curr.next
                print('None')
        print()

if __name__=='__main__':
    lfu=LFUCache(capacity=2)
    lfu.put(1,1)
    lfu.put(2,2)
    lfu.display()
    print(lfu.get(1))
    lfu.display()
    lfu.put(3, 3)
    lfu.display()
    print('For key 2:',lfu.get(2))
    lfu.display()
    print(lfu.get(3))
    lfu.display()
    print(f'Current size is: {lfu.size}')
    lfu.put(4,4)
    lfu.display()
    print('For key 1:',lfu.get(1))
    print(lfu.get(3))
    lfu.display()
    print(lfu.get(4))
    lfu.display()
