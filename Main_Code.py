import time
import sys
from collections import deque
from statistics import stdev
from statistics import mean

bfspath=[]  #for storing the path of BFS
dfspath=[]  #for storing the path of DFS
run_time_bfs = []
run_time_dfs = []
closed_set_size_bfs = []
closed_set_size_dfs = []

#function to move blank tile up
def moveUp(rootState,visitedNodes,Queue):

    newState=rootState[:] #creating shallow copy of rootState
    #finding the index of blank
    index=newState.index(0)
   
    if index not in [0,1,2]:
        swapvar=newState[index-3]       #moving blank tile up
        newState[index-3]=newState[index]
        newState[index]=swapvar
        for temp in visitedNodes:   #state detection: checking if node is in visited nodes
            if newState==temp.rootState:
                return None
        for temp in Queue:          #state detection: checking if node is in queue
            if newState==temp.rootState:
                return None
        return newState
    else:
        return None
#function to move blank tile down
def moveDown(rootState,visitedNodes,Queue):
   
    newState=rootState[:] #creating shallow copy of rootState
    #finding the index of blank
    index=newState.index(0)
    
    if index not in [6,7,8]:
        swapvar=newState[index+3]   #moving blank tile down
        newState[index+3]=newState[index]
        newState[index]=swapvar
        for temp in visitedNodes:   #state detection: checking if node is in visited nodes
            if newState==temp.rootState:
                return None
        for temp in Queue:           #state detection: checking if node is in queue
            if newState==temp.rootState:
                return None
        return newState
    else:
        return None

#function to move blank tile left   
def moveLeft(rootState,visitedNodes,Queue):
    
    newState=rootState[:] #creating shallow copy of rootState
    #finding the index of blank
    index=newState.index(0)
    if index not in [0,3,6]:
        swapvar=newState[index-1]   #moving blank tile left
        newState[index-1]=newState[index]
        newState[index]=swapvar
       
        for temp in visitedNodes:   #state detection: checking if node is in visited nodes
            if newState==temp.rootState:
                return None
        for temp in Queue:#state detection: checking if node is in queue
            if newState==temp.rootState:
                return None
        return newState
    else:
        return None

#function to move blank tile right
def moveRight(rootState, visitedNodes,Queue):
  
    newState=rootState[:] #creating shallow copy of rootState
    #finding the index of blank
    index=newState.index(0)
    if index not in [2,5,8]:        #moving tile right
        swapvar=newState[index+1]
        newState[index+1]=newState[index]
        newState[index]=swapvar
      
        for temp in visitedNodes:       #state detection: checking if node is in visited nodes
            if newState==temp.rootState:
                return None
        for temp in Queue:      #state detection: checking if node is in queue
            if newState==temp.rootState:
                return None
        #OutputProcedure(newState)
        return newState
    else:
        return None
        
    
#function to create children of a node
def successor(node, Queue,visitedNodes):
    
    children=deque()
   
    #for all position of blank trying up down left right moves
    children.append(makeNode(moveLeft(node.rootState,visitedNodes,Queue),node,"moveLeft",node.depth+1))#add the state after moving left
    
    children.append(makeNode(moveUp(node.rootState,visitedNodes,Queue),node,"moveUp",node.depth+1))#add the state after moving up
   
    children.append(makeNode(moveDown(node.rootState,visitedNodes,Queue),node,"moveDown",node.depth+1))#add the state after moving down
    
    children.append(makeNode(moveRight(node.rootState,visitedNodes,Queue),node,"moveRight",node.depth+1))#add the state after moving right
    #taking all the none from children using list comprehension
    children=[node for node in children if node.rootState!=None]
    
    return children


#class for node    
class Node:
    def __init__(self,rootState,parentState,movement,depth):
        self.rootState=rootState #stores root state
        self.parentState=parentState #stores parent state
        self.movement=movement #stores movement like "movedUp,movedDown,movedLeft,movedRight"
        self.depth=depth #stores depth of current state
        
#function to make node
def makeNode(rootState,parentState,movement,depth):
  
    return Node(rootState,parentState,movement,depth)


#bfs algorithm
def bfs(initial, goalState,limit):
    no=[]  
    num=0
    Queue=deque()   #queue for storing nodes
    visitedNodes=[] #for visited nodes
        
    Queue.append(makeNode(initial, None, None,0))
    num+=1
   
    while True: # execute untill u done with all child nodes
        if limit==0:
            closed_set_size_bfs.append(len(visitedNodes))
            return 0;
        if not Queue:    #if queue is empty
            closed_set_size_bfs.append(len(visitedNodes))
            return None;
       
        node=Queue.popleft()    #pop from front
        visitedNodes.append(node)   #storing visited nodes
        limit=limit-1 #to check the limit specified
        #finding all the child nodes of node(current root)
        if not testProcedure(node,goalState):
            no=successor(node,Queue,visitedNodes)
            
            Queue.extend(no)#node-new root storing child nodes in nodes(queue)
            num=num+len(no) #calculating the number of states generated
        else:
              #number of states generated: number of nodes which are explored
            list_of_moves=findPath_and_moves(node,"bfs",num)
            closed_set_size_bfs.append(len(visitedNodes))
            return list_of_moves

    

#function to create path       
def findPath_and_moves(node,name, num):
    if name=="bfs":
        bfspath.insert(0,node.rootState)   #to keep the track of path
    else:
        dfspath.insert(0,node.rootState)
    moves=[]
    temp=node
    while True: # to create list of movements
        moves.insert(0,temp.movement) #insert at start of list-length of moves will be total moves
        if temp.depth<=1:   #when initial and goal is same 
            break
        temp=temp.parentState
        if name=="bfs":
            bfspath.insert(0,temp.rootState)
        else:
            dfspath.insert(0,temp.rootState)
    #print "total number of moves:",num
    return moves

#function to test if search reached to goal state
def testProcedure(node,goalState):

    if node.rootState==goalState:
            return True
    return False    

#DFS     
def dfs( initialState,goalState,limit):
    #depth_limit=5
    no=[]   #for number of state generated purpose
    num=0
    Queue = deque() #act as stack by poping from end like a stack
    visitedNodes=[] #to keep track of visited nodes
    Queue.append( makeNode( initialState, None, None, 0 ) )
    num+=1
    while True:
        if limit==0:    #if search reaches limit
            closed_set_size_dfs.append(len(visitedNodes))
            return 0;
        if not Queue:#if stack is empty
            closed_set_size_dfs.append(len(visitedNodes))
            return None
        
        node = Queue.pop()
        visitedNodes.append(node)
        limit=limit-1 #limit=no of nodes tested with goal state
        #findingchild nodes if not reached the goal state
        if not testProcedure(node,goalState):
           
            no=successor( node, Queue,visitedNodes )
            Queue.extend(no)
            
            num=num+len(no)#for calculating the number of state generated
        else:
            
            list_of_moves=findPath_and_moves(node,"dfs",num)
            closed_set_size_dfs.append(len(visitedNodes))
            return list_of_moves
    
    

def OutputProcedure( state ): #for displaying the puzzle state
    for i in range(9):
        val = state[i]
        if val==0:
            print '.',
        else:
            print val,
        if (i+1)%3==0:
            print
#function to make a state
def makeState(nw, n, ne, w, c, e, sw, s, se):
    state=[]

    if nw!=0:
        state.append(nw)
    else:
        state.append(0)
    if n!=0:
        state.append(n)
    else:
        state.append(0)
    if ne!=0:
        state.append(ne)
    else:
        state.append(0)
    if w!=0:
        state.append(w)
    else:
        state.append(0)
    if c!=0:
        state.append(c)
    else:
        state.append(0)
    if e!=0:
        state.append(e)
    else:
        state.append(0)
    if sw!=0:
        state.append(sw)
    else:
        state.append(0)
    if s!=0:
        state.append(s)
    else:
        state.append(0)
    if se!=0:
        state.append(se)
    else:
        state.append(0)
    
    return state 
#function that cals bfs and depending upon te return prints the ouput-moves and path
def testBFS(initialState, goalState, limit):
    print "-------Breadth First Search-------------"
    no=0
    s=time.time()
    finalOutcome=bfs(initialState,goalState,limit)
    e=time.time();
    print "Time taken to solve:","%.3f" % (e - s),"secs"
    run_time_bfs.append(round(e-s, 3))

    if finalOutcome==None:
        print "No solution found"
    elif finalOutcome==[None]:
        print "Initial state is same as Goal state"
    elif finalOutcome==0:
        print "Reached the limit"
    else:
        #print "Movements of blank"
        #print finalOutcome
        print "Total",len(finalOutcome),"moves"
    '''if finalOutcome!=0:
        print "initial state"
        OutputProcedure(initialState)
        print "Path"
        move_count=len(bfspath)
        j=0
        while(move_count):
            OutputProcedure(bfspath[j])
            j=j+1
            move_count=move_count-1
   
    print "length of optimal path",len(bfspath)'''

#function that calls dfs and depending on return value display the output-path and moves
def testDFS(initialState, goalState, limit):
    print "-------Depth First Search-------------"
    s=time.time()
    Outcome=dfs(initialState,goalState,limit)
    e=time.time();
    print "Time taken to solve:","%.3f" % (e - s),"secs"
    run_time_dfs.append(round(e-s, 3))

    if Outcome==None:
        print "No solution found"
    elif Outcome==[None]:
        print "Initial state is same as Goal state"
    elif Outcome==0:
        print "Reached the limit"
    else:
        #print "Movements of blank"
        #print Outcome
        print "Total",len(Outcome),"moves"
    
    '''if(Outcome!=0):
        print "initial state"
        OutputProcedure(initialState)
        print "Path"
        move_count=len(dfspath)
        j=0
        while(move_count):
            OutputProcedure(dfspath[j])
            j=j+1
            move_count=move_count-1'''

def show_standard_deviations():
    print "Time Analysis for BFS is : " + str(round(mean(run_time_bfs),4)) + " " + u"\u00B1" + " " + str(round(stdev(run_time_bfs),4)) + "secs"
    print "Space Analysis for closed set size of BFS is : " + " " + str(round(mean(closed_set_size_bfs),4)) + " " + u"\u00B1" + str(round(stdev(closed_set_size_bfs),4))
    print "Time Analysis in run time for DFS is : " + str(round(mean(run_time_dfs),4)) + " " + u"\u00B1" + " " + str(round(stdev(run_time_dfs),4)) + "secs"
    print "Space Analysis for closed set size of DFS is : " + str(round(mean(closed_set_size_dfs),4)) + " " + u"\u00B1" + " " + str(round(stdev(closed_set_size_dfs),4))
    


#creating initial and goal state
for test in range(10):

    inp = raw_input().split()

    init=makeState(int(inp[0]), int(inp[1]), int(inp[2]), int(inp[3]), int(inp[4]), int(inp[5]), int(inp[6]), int(inp[7]), int(inp[8]))
    goal=makeState(1,2,3,4,5,6,7,8,0)

    out = raw_input().split()
    goal=makeState(int(out[0]), int(out[1]), int(out[2]), int(out[3]), int(out[4]), int(out[5]), int(out[6]), int(out[7]), int(out[8]))

    print "Goal State"
    OutputProcedure(goal)
    print "Initial State"
    OutputProcedure(init)


    print "***************Search Started******************"

    testBFS(init, goal, 2000)

    testDFS(init, goal, 2000)

    print "**************Search Completed******************"

print "\n"
print "**************"
print "|  ANALYSIS  |"
print "**************"
show_standard_deviations()


#print run_time_bfs
#print run_time_dfs
#print "Standard deviation in closed set size for bfs is : " + str(round(stdev(closed_set_size_bfs),4))
#print "Standard deviation in closed set size for dfs is : " + str(round(stdev(closed_set_size_dfs),4))

