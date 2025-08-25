import tkinter as tk
import random 

#added colors for the UI, better readability 
PRIMARY_BG = "#f5f7fa"
ACCENT_BG = "#e3eafc"
NODE_COLOR = "#a7c7e7"
NODE_VISITED = "#b6e2d3"
NODE_START = "#ffe066"
NODE_OUTLINE = "#3a506b"
TRACKER_BG = "#e3eafc"
TRACKER_BORDER = "#3a506b"
BUTTON_BG = "#5c7cfa"
BUTTON_FG = "#ffffff"
HIGHLIGHT_COLOR = "#ffd6a5"

DFSCode = """
def dfs(start):
    stack = [start]
    visited = set()
    order = []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for nbr in reversed(G[node]):
            if nbr not in visited:
                stack.append(nbr)
    return order
"""

def draw_directed_edge(canvas, x1, y1, x2, y2, r, **kw):
    dx, dy = x2 - x1, y2 - y1
    dist = (dx*dx + dy*dy) ** 0.5
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    sx, sy = x1 + ux * r, y1 + uy * r
    ex, ey = x2 - ux * r, y2 - uy * r
    canvas.create_line(sx, sy, ex, ey, arrow=tk.LAST, arrowshape=(16, 18, 8), width=2, **kw)

def draw_graph(canvas, nodes, edges, node_radius=20):
    for u, v in edges:
        x1, y1 = nodes[u]
        x2, y2 = nodes[v]
        draw_directed_edge(canvas, x1, y1, x2, y2, node_radius, fill="#adb5bd")

    for node_id, (x, y) in nodes.items():
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                           fill=NODE_COLOR, outline=NODE_OUTLINE, width=3, tags=f"node_{node_id}")
        canvas.create_text(x, y, text=str(node_id), font=("Arial", 16, "bold"), fill=NODE_OUTLINE, tags=f"label_{node_id}")

# ----------- Home Button Class ------------
class HomeButtonMixin:
    def add_home_button(self, master):
        home_button = tk.Button(self, text="🏠 Home", command=lambda: master.switch_frame(StartPage),
                                font=("Arial", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE, bd=0)
        home_button.place(x=10, y=10)

# ----------- Graph Node Class ------------
class GraphNode:
    def __init__(self, name, x, y, neighbors):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = neighbors
        self.visited = False

# ---------- Tracker panel ----------
class TrackerPanel(tk.Frame):
    def __init__(self, master, title="DFS Tracker"):
        super().__init__(master, bd=2, relief=tk.GROOVE, bg=TRACKER_BG, highlightbackground=TRACKER_BORDER, highlightthickness=2)
        tk.Label(self, text=title, font=("Arial", 13, "bold"), bg=TRACKER_BG, fg=NODE_OUTLINE).pack(pady=6)
        tk.Label(self, text="Stack (bottom → top)", bg=TRACKER_BG, fg=NODE_OUTLINE).pack(anchor="w", padx=8)
        self.stack_box = tk.Listbox(self, width=22, height=8, font=("Arial", 12), bg="#f8f9fa", fg=NODE_OUTLINE, bd=1, relief=tk.FLAT)
        self.stack_box.pack(padx=8, pady=4)
        tk.Label(self, text="Visited order", bg=TRACKER_BG, fg=NODE_OUTLINE).pack(anchor="w", padx=8)
        self.visited_box = tk.Listbox(self, width=22, height=8, font=("Arial", 12), bg="#f8f9fa", fg=NODE_OUTLINE, bd=1, relief=tk.FLAT)
        self.visited_box.pack(padx=8, pady=4)

    def set_stack(self, items):
        self.stack_box.delete(0, tk.END)
        for it in items:
            self.stack_box.insert(tk.END, it)

    def set_visited(self, items):
        self.visited_box.delete(0, tk.END)
        for it in items:
            self.visited_box.insert(tk.END, it)

# ----------- Main App ------------
class ProjectScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x650")
        self.title("DFS Visualizer")
        self.configure(bg=PRIMARY_BG)
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
        super().__init__(master, bg=PRIMARY_BG)
        self.add_home_button(master)
        tk.Label(self, text="DFS Visualizer", font=("Arial", 24, "bold"), bg=PRIMARY_BG, fg=NODE_OUTLINE).pack(pady=30)
        tk.Label(self, text="Welcome! Let's learn about Depth-First Search (DFS)", font=("Arial", 16), bg=PRIMARY_BG, fg=NODE_OUTLINE).pack(pady=10)
        tk.Button(self, text="Start Learning", command=lambda: master.switch_frame(WhatDFSPage),
                  font=("Arial", 14, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE, bd=0, padx=20, pady=8).pack(pady=20)

# ----------- What is DFS? Page ------------
class WhatDFSPage(tk.Frame, HomeButtonMixin):
    def __init__(self, master):
        super().__init__(master, bg=PRIMARY_BG)
        self.add_home_button(master)
        tk.Label(self, text="What is DFS?", font=("Arial", 20, "bold"), bg=PRIMARY_BG, fg=NODE_OUTLINE).pack(pady=18)
        explanation = (
            "Depth-First Search (DFS) is a fundamental graph traversal algorithm.\n"
            "It explores as far as possible along each branch before backtracking.\n\n"
            "Properties:\n"
            "- Works on trees and graphs\n"
            "- Uses a stack (or recursion)\n"
            "- Can be used to find connected components, paths, cycles, etc.\n\n"
            "Tree: A connected acyclic graph. Has a root node, and every node except the root has one parent.\n"
            "Graph: A collection of nodes (vertices) connected by edges. Can be directed or undirected.\n\n"
        )
        tk.Label(self, text=explanation, font=("Arial", 13), justify="left", bg=PRIMARY_BG, fg=NODE_OUTLINE).pack(pady=5)
        code_box = tk.Text(self, width=70, height=12, font=("Courier", 12), bg="#f8f9fa", fg=NODE_OUTLINE, insertbackground=NODE_OUTLINE, bd=2, relief=tk.GROOVE)
        code_box.insert("1.0", DFSCode.strip())
        code_box.config(state=tk.DISABLED)
        code_box.pack(pady=10, padx=10)
        tk.Button(self, text="Tree Problem", command=lambda: master.switch_frame(PracticeProblemTreePage),
                  font=("Arial", 13, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE, bd=0, padx=12, pady=6).pack(pady=5)
        tk.Button(self, text="Graph Problem", command=lambda: master.switch_frame(GraphProblemPage),
                  font=("Arial", 13, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE, bd=0, padx=12, pady=6).pack(pady=5)

# ----------- Practice Problem Tree Page ------------
class PracticeProblemTreePage(tk.Frame, HomeButtonMixin):
    def __init__(self, master):
        super().__init__(master, bg=PRIMARY_BG)
        self.add_home_button(master)
        tk.Label(self, text="Step through DFS!", font=("Arial", 18, "bold"), bg=PRIMARY_BG, fg=NODE_OUTLINE).pack(pady=10)
        self.text_label = tk.Label(self, text="", font=("Arial", 14), bg=PRIMARY_BG, fg=NODE_OUTLINE)
        self.text_label.pack(pady=10)
        self.canvas = tk.Canvas(self, width=600, height=400, bg=ACCENT_BG, bd=0, highlightthickness=0)
        self.canvas.pack()

        self.tracker = TrackerPanel(self, title="DFS Tracker")
        self.tracker.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

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
            {"node": 0, "text": "We start at node 0 because it is the root.", "fill": NODE_START, "outline": NODE_OUTLINE},
            {"node": 2, "text": "Visit node 2 as it is the left-most child node.", "fill": NODE_VISITED, "outline": NODE_OUTLINE},
            {"node": 4, "text": "Visit node 4 next.", "fill": NODE_VISITED, "outline": NODE_OUTLINE},
            {"node": 4, "text": "Node 4 is a leaf node so we backtrack up to node 2.", "fill": NODE_VISITED},
            {"node": 2, "text": "Node 2 has no more unvisited child nodes so we backtrack.", "fill": NODE_VISITED, "outline": NODE_OUTLINE},
            {"node": 3, "text": "Visit the next child node from 0, node 3.", "fill": NODE_VISITED, "outline": NODE_OUTLINE},
            {"node": 3, "text": "Node 3 is a leaf node so we backtrack to node 0.", "fill": NODE_VISITED, "outline": NODE_OUTLINE},
            {"node": 1, "text": "Visit the last child of node 0, node 1.", "fill": NODE_VISITED, "outline": NODE_OUTLINE},
            {"node": 1, "text": "All nodes in the tree graph have been visited.", "fill": NODE_VISITED, "outline": NODE_OUTLINE},
        ]

        self.current_step = -1

        button_frame = tk.Frame(self, bg=PRIMARY_BG)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="← Back", command=self.prev_step,
                  font=("Arial", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE, bd=0, padx=12, pady=6).pack(side="left", padx=10)
        tk.Button(button_frame, text="→ Next", command=self.next_step,
                  font=("Arial", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE, bd=0, padx=12, pady=6).pack(side="left", padx=10)
        tk.Button(self, text="Try on your own!", command=lambda: master.switch_frame(DFSPage),
                  font=("Arial", 13, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE, bd=0, padx=12, pady=6).pack(pady=10)
        self.code_text = tk.Text(self, wrap=tk.WORD, width=50, height=15, font=("Courier New", 11), bg="#f8f9fa", fg=NODE_OUTLINE, insertbackground=NODE_OUTLINE, bd=2, relief=tk.GROOVE)
        self.code_text.pack(side=tk.RIGHT, padx=50)
        self.code_text.insert(tk.END, DFSCode)
        self.code_text.config(state=tk.DISABLED)

        self.step_to_code_line = {
            0: [2,3],
            1: [4],
            2: [5,6],
            3: [7],
            4: [6,7],
            5: [8,9,10],
            6: [5,6,7],
            7: [5,6,7],
            8: [11]
        }

        self.tracker_stack_steps = [
            [0], [2,0], [4,2,0], [2,0], [0], [3,0], [0], [1], []
        ]
        self.tracker_visited_steps = [
            [0], [0,2], [0,2,4], [0,2,4], [0,2,4], [0,2,4,3], [0,2,4,3], [0,2,4,3,1], [0,2,4,3,1]
        ]

    def highlight_code_line(self, line_num):
        self.code_text.config(state=tk.NORMAL)
        self.code_text.tag_remove("highlight", "1.0", tk.END)
        for line_num in line_num:
            if line_num >= 1:
                self.code_text.tag_add("highlight", f"{line_num}.0", f"{line_num}.end")
        self.code_text.tag_config("highlight", background=HIGHLIGHT_COLOR)
        self.code_text.config(state=tk.DISABLED)

    def highlight_node(self, node_id, fill_color=NODE_VISITED, outline_color=NODE_OUTLINE):
        self.canvas.itemconfig(f"node_{node_id}", fill=fill_color, outline=outline_color)

    def reset_all_nodes(self):
        for node_id in self.nodes:
            self.canvas.itemconfig(f"node_{node_id}", fill=NODE_COLOR, outline=NODE_OUTLINE)

    def next_step(self):
        if self.current_step + 1 < len(self.steps):
            self.current_step += 1
            step = self.steps[self.current_step]
            self.text_label.config(text=step["text"])
            self.highlight_node(step["node"], step["fill"], step.get("outline", NODE_OUTLINE))
            self.highlight_code_line(self.step_to_code_line[self.current_step])
            self.tracker.set_stack(self.tracker_stack_steps[self.current_step] if self.current_step < len(self.tracker_stack_steps) else [])
            self.tracker.set_visited(self.tracker_visited_steps[self.current_step] if self.current_step < len(self.tracker_visited_steps) else [])

    def prev_step(self):
        if self.current_step >= 0:
            self.code_text.config(state=tk.NORMAL)
            self.code_text.tag_remove("highlight", "1.0", tk.END)
            self.code_text.config(state=tk.DISABLED)
            prev_node = self.steps[self.current_step]["node"]
            self.highlight_node(prev_node, NODE_COLOR, NODE_OUTLINE)
            self.current_step -= 1
            if self.current_step >= 0:
                step = self.steps[self.current_step]
                self.text_label.config(text=step["text"])
                self.tracker.set_stack(self.tracker_stack_steps[self.current_step] if self.current_step < len(self.tracker_stack_steps) else [])
                self.tracker.set_visited(self.tracker_visited_steps[self.current_step] if self.current_step < len(self.tracker_visited_steps) else [])
            else:
                self.text_label.config(text="")
                self.tracker.set_stack([])
                self.tracker.set_visited([])

# ----------- Graph Practice Problem Page -----------
class GraphProblemPage(tk.Frame, HomeButtonMixin):
    def __init__(self, master):
        super().__init__(master, bg=PRIMARY_BG)
        self.add_home_button(master)
        tk.Label(self, text="DFS on an Undirected Graph", font=("Arial", 18, "bold"), bg=PRIMARY_BG, fg=NODE_OUTLINE).pack(pady=10)
        self.text_label = tk.Label(self, text="", font=("Arial", 14), bg=PRIMARY_BG, fg=NODE_OUTLINE)
        self.text_label.pack(pady=10)
        self.canvas = tk.Canvas(self, width=600, height=400, bg=ACCENT_BG, bd=0, highlightthickness=0)
        self.canvas.pack()

        self.tracker = TrackerPanel(self, title="DFS Tracker")
        self.tracker.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.code_text = tk.Text(self, wrap=tk.WORD, width=50, height=15, font=("Courier New", 11), bg="#f8f9fa", fg=NODE_OUTLINE, insertbackground=NODE_OUTLINE, bd=2, relief=tk.GROOVE)
        self.code_text.pack(side=tk.RIGHT, padx=50)
        self.code_text.insert(tk.END, DFSCode)
        self.code_text.config(state=tk.DISABLED)

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
            {"node": 0, "text": "Start DFS at node 0.", "fill": NODE_START, "outline": NODE_OUTLINE},
            {"node": 1, "text": "Visit neighbor node 1 from 0.", "fill": NODE_VISITED, "outline": NODE_OUTLINE},
            {"node": 2, "text": "Backtrack and visit node 2 from 0.", "fill": NODE_VISITED, "outline": NODE_OUTLINE},
            {"node": 3, "text": "Visit neighbor node 3 from 2.", "fill": NODE_VISITED, "outline": NODE_OUTLINE},
            {"node": 4, "text": "Backtrack to 2, then visit node 4.", "fill": NODE_VISITED, "outline": NODE_OUTLINE},
        ]

        self.current_step = -1

        self.tracker_stack_steps = [
            [0], [1,0], [2,0], [3,2,0], [4,2,0]
        ]
        self.tracker_visited_steps = [
            [0], [0,1], [0,1,2], [0,1,2,3], [0,1,2,3,4]
        ]

        self.step_to_code_line = {
            0: [2,3],
            1: [4,5],
            2: [6,7],
            3: [8,9,10],
            4: [11]
        }

        button_frame = tk.Frame(self, bg=PRIMARY_BG)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="← Back", command=self.prev_step,
                  font=("Arial", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE, bd=0, padx=12, pady=6).pack(side="left", padx=10)
        tk.Button(button_frame, text="→ Next", command=self.next_step,
                  font=("Arial", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE, bd=0, padx=12, pady=6).pack(side="left", padx=10)
        tk.Button(self, text="Try on your own!", command=lambda: master.switch_frame(DFSPage),
                  font=("Arial", 13, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE, bd=0, padx=12, pady=6).pack(pady=10)

    def highlight_code_line(self, line_num):
        self.code_text.config(state=tk.NORMAL)
        self.code_text.tag_remove("highlight", "1.0", tk.END)
        for ln in line_num:
            if ln >= 1:
                self.code_text.tag_add("highlight", f"{ln}.0", f"{ln}.end")
        self.code_text.tag_config("highlight", background=HIGHLIGHT_COLOR)
        self.code_text.config(state=tk.DISABLED)

    def highlight_node(self, node_id, fill_color=NODE_VISITED, outline_color=NODE_OUTLINE):
        self.canvas.itemconfig(f"node_{node_id}", fill=fill_color, outline=outline_color)

    def next_step(self):
        if self.current_step + 1 < len(self.steps):
            self.current_step += 1
            step = self.steps[self.current_step]
            self.text_label.config(text=step["text"])
            self.highlight_node(step["node"], step["fill"], step["outline"])
            self.tracker.set_stack(self.tracker_stack_steps[self.current_step] if self.current_step < len(self.tracker_stack_steps) else [])
            self.tracker.set_visited(self.tracker_visited_steps[self.current_step] if self.current_step < len(self.tracker_visited_steps) else [])
            self.highlight_code_line(self.step_to_code_line[self.current_step])

    def prev_step(self):
        if self.current_step >= 0:
            prev_node = self.steps[self.current_step]["node"]
            self.highlight_node(prev_node, NODE_COLOR, NODE_OUTLINE)
            self.current_step -= 1
            if self.current_step >= 0:
                self.text_label.config(text=self.steps[self.current_step]["text"])
                self.tracker.set_stack(self.tracker_stack_steps[self.current_step] if self.current_step < len(self.tracker_stack_steps) else [])
                self.tracker.set_visited(self.tracker_visited_steps[self.current_step] if self.current_step < len(self.tracker_visited_steps) else [])
                self.highlight_code_line(self.step_to_code_line[self.current_step])
            else:
                self.text_label.config(text="")
                self.tracker.set_stack([])
                self.tracker.set_visited([])
                self.code_text.config(state=tk.NORMAL)
                self.code_text.tag_remove("highlight", "1.0", tk.END)
                self.code_text.config(state=tk.DISABLED)

# ----------- DFS Graph Page ------------
class DFSPage(tk.Frame, HomeButtonMixin):
    def __init__(self, master):
        super().__init__(master, bg=PRIMARY_BG)
        self.add_home_button(master)

        header = tk.Frame(self, bg=PRIMARY_BG)
        header.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(header, text="DFS Game: Pick nodes in DFS order", font=("Arial", 16, "bold"), bg=PRIMARY_BG, fg=NODE_OUTLINE).pack(side="left")
        self.score_label = tk.Label(header, text="Rounds cleared: 0", font=("Arial", 12), bg=PRIMARY_BG, fg=NODE_OUTLINE)
        self.score_label.pack(side="right")

        # Feedback / instructions
        self.feedback = tk.Label(self, text="", font=("Arial", 13), bg=PRIMARY_BG, fg=NODE_OUTLINE, wraplength=780, justify="left")
        self.feedback.pack(pady=(6, 8))

        self.tracker = TrackerPanel(self, title="Your Progress")
        self.tracker.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        self.canvas = tk.Canvas(self, width=800, height=500, bg=ACCENT_BG, bd=0, highlightthickness=0)
        self.canvas.pack(padx=10, pady=4)
        self.graph = {} 
        self.edges = [] 
        self.expected_order = []
        self.current_index = 0 
        self.rounds_cleared = 0
        self.canvas.bind("<Button-1>", self.on_click)
        controls = tk.Frame(self, bg=PRIMARY_BG)
        controls.pack(pady=8)
        tk.Button(controls, text="New Graph", command=self.new_round,
                  font=("Arial", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE,
                  bd=0, padx=12, pady=6).pack(side="left", padx=6)
        tk.Button(controls, text="Reveal Order", command=self.reveal_order,
                  font=("Arial", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE,
                  bd=0, padx=12, pady=6).pack(side="left", padx=6)
        tk.Button(controls, text="Back", command=lambda: master.switch_frame(StartPage),
                  font=("Arial", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  activebackground=ACCENT_BG, activeforeground=NODE_OUTLINE,
                  bd=0, padx=12, pady=6).pack(side="left", padx=6)
        self.new_round()

    # ---------- Round lifecycle ----------
    def new_round(self):
        self.clear_canvas()
        self.graph = self.generate_connected_graph()
        self.edges = self.build_edge_list(self.graph)
        self.draw_current_graph()
        start = random.choice(list(self.graph.keys()))
        self.expected_order = self.compute_dfs_order(start)
        self.current_index = 0
        self.tracker.set_visited([])
        self.tracker.set_stack([]) 
        self.feedback.config(text=f"Start at node {start}. Pick nodes in correct DFS order.\n" f"Tip: DFS uses a stack; we visit as deep as possible before backtracking.")

    def next_round(self):
        self.rounds_cleared += 1
        self.score_label.config(text=f"Rounds cleared: {self.rounds_cleared}")
        self.feedback.config(text="✅ Correct! Generating a new graph...")
        self.after(800, self.new_round)

    # ---------- Graph generation & drawing ----------
    def generate_connected_graph(self):
        n = random.randint(5, 7)
        names = [chr(ord('A') + i) for i in range(n)]
        # Place nodes on a loose grid
        positions = self.random_positions(n)

        # Start with a tree to ensure connectivity
        adj = {name: set() for name in names}
        for i in range(1, n):
            u = names[i]
            v = random.choice(names[:i])
            adj[u].add(v)
            adj[v].add(u)

        # Add a few extra edges (avoid multi-edges/self-loops)
        extra_edges = random.randint(1, max(1, n // 2))
        attempted = 0
        while extra_edges > 0 and attempted < 20:
            u, v = random.sample(names, 2)
            attempted += 1
            if v not in adj[u]:
                adj[u].add(v)
                adj[v].add(u)
                extra_edges -= 1

        graph = {}
        for name in names:
            x, y = positions[name]
            neighbors = sorted(list(adj[name]))
            graph[name] = GraphNode(name, x, y, neighbors)
            graph[name].visited = False
        return graph

    def random_positions(self, n):
        # grid points within canvas bounds
        cols, rows = 3, max(2, (n + 2) // 3)
        xs = [120, 300, 480, 660][:cols]
        ys = [110, 230, 350, 440][:rows]
        spots = [(x, y) for y in ys for x in xs]
        random.shuffle(spots)
        names = [chr(ord('A') + i) for i in range(n)]
        return {name: spots[i] for i, name in enumerate(names)}

    def build_edge_list(self, graph):
        edges = []
        for u, node in graph.items():
            for v in node.neighbors:
                edges.append((u, v))
        return edges

    def draw_current_graph(self):
        # Draw edges
        for u, v in self.edges:
            n1, n2 = self.graph[u], self.graph[v]
            draw_directed_edge(self.canvas, n1.x, n1.y, n2.x, n2.y, 20, fill="#adb5bd")
        # Draw nodes
        for node in self.graph.values():
            self.canvas.create_oval(node.x - 20, node.y - 20, node.x + 20, node.y + 20, fill=NODE_COLOR, outline=NODE_OUTLINE, width=3, tags=node.name)
            self.canvas.create_text(node.x, node.y, text=node.name, font=("Arial", 14, "bold"), fill=NODE_OUTLINE, tags=node.name)

    def clear_canvas(self):
        self.canvas.delete("all")

    # ---------- DFS order (ground truth) ----------
    def compute_dfs_order(self, start):
        stack = [start]
        visited = set()
        order = []
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            nbrs = list(self.graph[node].neighbors)
            for nbr in reversed(nbrs):
                if nbr not in visited:
                    stack.append(nbr)
        return order

    # ---------- Interaction ----------
    def on_click(self, event):
        clicked = self.get_node_at(event.x, event.y)
        if not clicked:
            return

        # Already visited?
        if clicked.visited:
            self.flash_feedback(f"⚠️ {clicked.name} already visited. Next expected: {self.expected_order[self.current_index]}")
            return

        expected = self.expected_order[self.current_index]

        if clicked.name != expected:
            # Wrong pick — flash node and message
            self.flash_node(clicked.name)
            self.flash_feedback(f"❌ Not quite. Try node {expected} next.")
            return

        # Correct pick
        clicked.visited = True
        self.canvas.itemconfig(clicked.name, fill=NODE_VISITED)
        visited_order = [n for n in self.expected_order[:self.current_index + 1]]
        self.tracker.set_visited(visited_order)
        self.current_index += 1

        if self.current_index == len(self.expected_order):
            self.next_round()

    def get_node_at(self, x, y):
        for node in self.graph.values():
            if (node.x - 20 <= x <= node.x + 20) and (node.y - 20 <= y <= node.y + 20):
                return node
        return None

    # ---------- UX helpers ----------
    def flash_node(self, tag_name):
        self.canvas.itemconfig(tag_name, fill="#ffadad")
        self.after(220, lambda: self.canvas.itemconfig(tag_name, fill=NODE_COLOR if not self.graph[tag_name].visited else NODE_VISITED))

    def flash_feedback(self, msg):
        self.feedback.config(text=msg)
        orig = self.feedback.cget("bg")
        self.feedback.config(bg="#fff3cd")
        self.after(250, lambda: self.feedback.config(bg=PRIMARY_BG))

    def reveal_order(self):
        self.feedback.config(text=f"True DFS order: {' → '.join(self.expected_order)}")

if __name__ == "__main__":
    app = ProjectScreen()
    app.mainloop()
