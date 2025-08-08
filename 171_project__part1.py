import tkinter as tk

def draw_graph(canvas, nodes, edges, node_radius=20):
    for u, v in edges:
        x1, y1 = nodes[u]
        x2, y2 = nodes[v]
        canvas.create_line(x1, y1, x2, y2, width=2)

    for node_id, (x, y) in nodes.items():
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="honeydew", outline="black", tags=f"node_{node_id}")
        canvas.create_text(x, y, text=str(node_id), font=("Arial", 14), tags=f"label_{node_id}")

# ----------- Home Button Class ------------
class HomeButtonMixin:
    def add_home_button(self, master):
        home_button = tk.Button(self, text="🏠 Home", command=lambda: master.switch_frame(StartPage))
        home_button.place(x=10, y=10)  # Top-left corner

# ----------- Graph Node Class ------------
class GraphNode:
    def __init__(self, name, x, y, neighbors):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = neighbors
        self.visited = False

# ----------- Main App ------------
class ProjectScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("DFS Visualizer")
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill='both', expand=True)

# ----------- Start Page ------------
class StartPage(tk.Frame, HomeButtonMixin):
    def __init__(self, master):
        super().__init__(master)
        self.add_home_button(master)
        tk.Label(self, text="Welcome, Let's learn about DFS!", font=("Arial", 16)).pack(pady=20)
        tk.Button(self, text="Start Learning", command=lambda: master.switch_frame(WhatDFSPage)).pack()

# ----------- What is DFS? Page ------------
class WhatDFSPage(tk.Frame, HomeButtonMixin):
    def __init__(self, master):
        super().__init__(master)
        self.add_home_button(master)
        tk.Label(self, text="What is DFS?", font=("Arial", 16)).pack(pady=20)
        tk.Label(self, text="text about what it is maybe some code idk", font=("Arial", 16)).pack(pady=20)
        tk.Button(self, text="Tree Problem", command=lambda: master.switch_frame(PracticeProblemTreePage)).pack()
        tk.Button(self, text="Graph Problem", command=lambda: master.switch_frame(GraphProblemPage)).pack()

#  ----------- Practice Problem Tree Page ------------
class PracticeProblemTreePage(tk.Frame, HomeButtonMixin):
    def __init__(self, master):
        super().__init__(master)
        self.add_home_button(master)
        tk.Label(self, text="Step through DFS!", font=("Arial", 16)).pack(pady=10)
        self.text_label = tk.Label(self, text="", font=("Arial", 14))
        self.text_label.pack(pady=10)
        self.canvas = tk.Canvas(self, width=600, height=400, bg="white")
        self.canvas.pack()
        
        self.nodes = {
            0: (300, 100),
            1: (400, 200),
            2: (200, 200),
            3: (300, 250),
            4: (150, 300),
        }
        
        self.edges = [(0, 1), (0, 2), (0, 3), (2, 4)]
        draw_graph(self.canvas, self.nodes, self.edges)
        
        self.steps = [
            {"node": 0, "text": "We start at node 0 beacuse it is the root. The root of a node is the \ntopmost node in the hierarchical structure. It's the node that has no parent, \n meaning it's the entry point to the entire tree.", "fill": "lightblue", "outline": "red"},
            {"node": 2, "text": "Then visit node 2 as it is the left-most child node. ", "fill": "lightgreen", "outline": "red"},
            {"node": 4, "text": "Since node 2 is not a lead node, we visit node 4 next.", "fill": "lightgreen", "outline": "red"},
            {"node": 4, "text": "Node 4 is a leaf node so we backtrack up to node 2.", "fill": "lightgreen"},
            {"node": 2, "text": "Node 2 does not have anymore unvisited child nodes so we backtrack again.", "fill": "lightgreen", "outline": "red"},
            {"node": 3, "text": "Now, we visit the next child node from 0 which is node 3.", "fill": "lightgreen", "outline": "red"},
            {"node": 3, "text": "Node 3 is a leaf node so we bcktrack to node 0.", "fill": "lightgreen", "outline": "red"},
            {"node": 1, "text": "Now, we visit the last child of node 0 which is node 1.", "fill": "lightgreen", "outline": "red"},
            {"node": 1, "text": "All nodes in the tree graph have been visited.", "fill": "lightgreen", "outline": "red"},
        ]
        
        self.current_step = -1  
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="← Back", command=self.prev_step).pack(side="left", padx=10)
        tk.Button(button_frame, text="→ Next", command=self.next_step).pack(side="left", padx=10)
        tk.Button(self, text="Try on your own!", command=lambda: master.switch_frame(DFSPage)).pack(pady=10)

    def highlight_node(self, node_id, fill_color="lightgreen", outline_color="black"):
        self.canvas.itemconfig(f"node_{node_id}", fill=fill_color, outline=outline_color)

    
    def reset_all_nodes(self):
        for node_id in self.nodes:
            self.canvas.itemconfig(f"node_{node_id}", fill="honeydew", )
    
    def next_step(self):
        if self.current_step + 1 < len(self.steps):
            self.current_step += 1
            step = self.steps[self.current_step]
            self.text_label.config(text=step["text"])
            self.highlight_node(step["node"], step["fill"], step["outline"])
    
    def prev_step(self):
        if self.current_step >= 0:
            prev_node = self.steps[self.current_step]["node"]
            self.highlight_node(prev_node, "honeydew", "black")
            self.current_step -= 1
            if self.current_step >= 0:
                step = self.steps[self.current_step]
                self.text_label.config(text=step["text"])
            else:
                self.text_label.config(text="")

# ----------- Graph Practice Problem Page -----------
class GraphProblemPage(tk.Frame, HomeButtonMixin):
    def __init__(self, master):
        super().__init__(master)
        self.add_home_button(master)
        tk.Label(self, text="DFS on an Undirected Graph", font=("Arial", 16)).pack(pady=10)
        self.text_label = tk.Label(self, text="", font=("Arial", 14))
        self.text_label.pack(pady=10)
        self.canvas = tk.Canvas(self, width=600, height=400, bg="white")
        self.canvas.pack()

        self.nodes = {
            0: (150, 300),
            1: (150, 100),
            2: (300, 200),
            3: (300, 350),
            4: (450, 200),
        }
        self.edges = [
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 3),
            (2, 4),
        ]

        draw_graph(self.canvas, self.nodes, self.edges)

        self.steps = [
            {"node": 0, "text": "Start DFS at node 0.", "fill": "lightblue", "outline": "red"},
            {"node": 1, "text": "Visit neighbor node 1 from 0.", "fill": "lightgreen", "outline": "red"},
            {"node": 2, "text": "Backtrack and visit node 2 from 0.", "fill": "lightgreen", "outline": "red"},
            {"node": 3, "text": "Visit neighbor node 3 from 2.", "fill": "lightgreen", "outline": "red"},
            {"node": 4, "text": "Backtrack to 2, then visit node 4.", "fill": "lightgreen", "outline": "red"},
        ]

        self.current_step = -1
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="← Back", command=self.prev_step).pack(side="left", padx=10)
        tk.Button(button_frame, text="→ Next", command=self.next_step).pack(side="left", padx=10)
        tk.Button(self, text="Try on your own!", command=lambda: master.switch_frame(DFSPage)).pack(pady=10)

    def highlight_node(self, node_id, fill_color="lightgreen", outline_color="black"):
        self.canvas.itemconfig(f"node_{node_id}", fill=fill_color, outline=outline_color)

    def next_step(self):
        if self.current_step + 1 < len(self.steps):
            self.current_step += 1
            step = self.steps[self.current_step]
            self.text_label.config(text=step["text"])
            self.highlight_node(step["node"], step["fill"], step["outline"])

    def prev_step(self):
        if self.current_step >= 0:
            prev_node = self.steps[self.current_step]["node"]
            self.highlight_node(prev_node, "honeydew", "black")
            self.current_step -= 1
            if self.current_step >= 0:
                self.text_label.config(text=self.steps[self.current_step]["text"])
            else:
                self.text_label.config(text="")


# ----------- DFS Graph Page ------------
class DFSPage(tk.Frame, HomeButtonMixin):
    def __init__(self, master):
        super().__init__(master)
        self.add_home_button(master)
        tk.Label(self, text="Click on a node to perform DFS", font=("Arial", 14)).pack()
        self.canvas = tk.Canvas(self, width=800, height=500, bg='white')
        self.canvas.pack()
        self.graph = self.create_graph()
        self.draw_graph()
        self.stack = []
        self.visited_order = []
        self.canvas.bind("<Button-1>", self.on_click)
        tk.Button(self, text="Back", command=lambda: master.switch_frame(StartPage)).pack(pady=10)

    def create_graph(self):
        return {
            'A': GraphNode('A', 100, 100, ['B', 'C']),
            'B': GraphNode('B', 250, 100, ['D']),
            'C': GraphNode('C', 100, 250, []),
            'D': GraphNode('D', 250, 250, [])
        }

    def draw_graph(self):
        for node in self.graph.values():
            for neighbor in node.neighbors:
                n2 = self.graph[neighbor]
                self.canvas.create_line(node.x, node.y, n2.x, n2.y, fill="gray", width=2)
        for node in self.graph.values():
            self.canvas.create_oval(node.x - 20, node.y - 20, node.x + 20, node.y + 20,
                                    fill='lightgray', tags=node.name)
            self.canvas.create_text(node.x, node.y, text=node.name, font=("Arial", 12), tags=node.name)

    def on_click(self, event):
        clicked_node = self.get_node_at(event.x, event.y)
        if clicked_node:
            if not self.stack:
                self.stack.append(clicked_node.name)
                self.process_dfs()
            else:
                print("DFS is already running!")

    def get_node_at(self, x, y):
        for node in self.graph.values():
            if (node.x - 20 <= x <= node.x + 20) and (node.y - 20 <= y <= node.y + 20):
                return node
        return None

    def process_dfs(self):
        if not self.stack:
            print("DFS Complete!")
            return
        node_name = self.stack.pop()
        node = self.graph[node_name]
        if node.visited:
            self.after(500, self.process_dfs)
            return
        node.visited = True
        self.visited_order.append(node_name)
        self.canvas.itemconfig(node.name, fill='lightgreen')
        print(f"Visited: {node_name}")
        for neighbor in reversed(node.neighbors):
            if not self.graph[neighbor].visited:
                self.stack.append(neighbor)
        self.after(500, self.process_dfs)


if __name__ == "__main__":
    app = ProjectScreen()
    app.mainloop()
