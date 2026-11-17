import os
import tkinter as tk
from tkinter import filedialog, ttk


BACKGROUND = "#2B2B28"
FOREGROUND = "#F2F2F2"
FIELD = "#3C3C38"
ACCENT = "#5C5C56"

_ROOT = None


def get_root():
    global _ROOT
    if _ROOT is None:
        _ROOT = tk.Tk()
        _ROOT.withdraw()
        style = ttk.Style(_ROOT)
        style.theme_use("clam")
        style.configure("App.TFrame", background=BACKGROUND)
        style.configure("App.TLabel", background=BACKGROUND, foreground=FOREGROUND)
        style.configure("App.TButton", padding=(8, 4))
        style.configure("App.TCheckbutton", background=BACKGROUND, foreground=FOREGROUND)
        style.map(
            "App.TCheckbutton",
            background=[("active", BACKGROUND), ("disabled", BACKGROUND)],
            foreground=[("disabled", "#8A8A84")],
        )
        style.configure("Treeview", rowheight=22, fieldbackground=FIELD, background=FIELD, foreground=FOREGROUND)
        style.configure("Treeview.Heading", padding=4)
    return _ROOT


def text(value, background=None, width=None):
    return {"type": "text", "text": value, "background": background, "width": width}


def button(label, key=None, disabled=False):
    return {"type": "button", "text": label, "key": key or label, "disabled": disabled}


def input_box(key, default="", enable_events=False, width=48, expand=False):
    return {
        "type": "input",
        "key": key,
        "default": default,
        "enable_events": enable_events,
        "width": width,
        "expand": expand,
    }


def file_browse(file_types=None, initial_folder=None):
    return {"type": "file", "file_types": file_types or [], "initial_folder": initial_folder}


def folder_browse():
    return {"type": "folder"}


def checkbox(label, key, default=False, disabled=False, enable_events=False):
    return {
        "type": "checkbox",
        "text": label,
        "key": key,
        "default": default,
        "disabled": disabled,
        "enable_events": enable_events,
    }


def table(key, headings, visible=True, height=12):
    return {"type": "table", "key": key, "headings": headings, "visible": visible, "height": height}


def multiline(key, default="", width=60, height=6):
    return {"type": "multiline", "key": key, "default": default, "width": width, "height": height}


def listbox(key, items, default=None, height=3, width=16):
    return {
        "type": "listbox",
        "key": key,
        "items": items,
        "default": default if default is not None else (items[:1] if items else []),
        "height": height,
        "width": width,
    }


def _dialog_parent():
    root = get_root()
    for child in reversed(root.winfo_children()):
        try:
            if child.winfo_viewable():
                return child
        except tk.TclError:
            continue
    return root


def popup_text(message, title="Done", default_text=""):
    parent = _dialog_parent()
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.configure(bg=BACKGROUND)
    dialog.transient(parent)
    ttk.Label(dialog, text=message, style="App.TLabel", wraplength=640, justify="left").pack(
        anchor="w", padx=12, pady=(12, 6)
    )
    entry = tk.Entry(dialog, bg=FIELD, fg=FOREGROUND, insertbackground=FOREGROUND, relief="flat")
    entry.insert(0, default_text)
    entry.pack(fill="x", padx=12, pady=6)
    entry.focus_set()
    entry.selection_range(0, "end")

    chosen = {"value": default_text}

    def accept():
        chosen["value"] = entry.get()
        dialog.destroy()

    ttk.Button(dialog, text="OK", style="App.TButton", command=accept).pack(anchor="e", padx=12, pady=(0, 12))
    dialog.bind("<Return>", lambda _event: accept())
    dialog.protocol("WM_DELETE_WINDOW", accept)
    dialog.grab_set()
    dialog.wait_window()
    return chosen["value"]


class Element:
    def __init__(self, kind, widget, variable=None, holder=None):
        self.kind = kind
        self.widget = widget
        self.variable = variable
        self.holder = holder

    def get(self):
        if self.kind == "input":
            return self.widget.get()
        if self.kind == "checkbox":
            return bool(self.variable.get())
        if self.kind == "multiline":
            return self.widget.get("1.0", "end-1c")
        if self.kind == "listbox":
            selected = [self.widget.get(index) for index in self.widget.curselection()]
            if selected:
                return selected
            current = self.variable.get() if self.variable is not None else ""
            return [current] if current else []
        return None

    def update(self, disabled=None, value=None, values=None, visible=None):
        if disabled is not None and self.kind in ("button", "checkbox", "input", "listbox"):
            self.widget.configure(state="disabled" if disabled else "normal")
        if self.kind == "input" and value is not None:
            self.widget.configure(state="normal")
            self.widget.delete(0, "end")
            self.widget.insert(0, value)
        if self.kind == "multiline" and value is not None:
            self.widget.configure(state="normal")
            self.widget.delete("1.0", "end")
            self.widget.insert("1.0", value)
        if self.kind == "checkbox" and value is not None:
            self.variable.set(bool(value))
        if self.kind == "table":
            if values is not None:
                self.widget.delete(*self.widget.get_children())
                columns = len(self.widget["columns"])
                for row in values:
                    cells = ["" if cell is None else str(cell) for cell in row]
                    if len(cells) < columns:
                        cells.extend([""] * (columns - len(cells)))
                    self.widget.insert("", "end", values=cells[:columns])
            if visible is not None and self.holder is not None:
                if visible:
                    self.holder.pack(fill="both", expand=True, pady=4)
                else:
                    self.holder.pack_forget()


def _contains_type(row, kinds):
    for item in row:
        if isinstance(item, list):
            if _contains_type(item, kinds):
                return True
        elif isinstance(item, dict) and item.get("type") in kinds:
            return True
    return False


class CreateWindow:
    resizable = True

    def create(self, title, layout, size):
        return AppWindow(title, layout, size)


class AppWindow:
    def __init__(self, title, layout, size):
        root = get_root()
        self.top = tk.Toplevel(root)
        self.top.withdraw()
        self.top.title(title)
        self.top.configure(bg=BACKGROUND)
        self.top.resizable(True, True)
        self.elements = {}
        self._pending = None
        self._closed = False
        self._tick = tk.IntVar(master=self.top, value=0)
        self.top.protocol("WM_DELETE_WINDOW", self._on_close)

        self.body = tk.Frame(self.top, bg=BACKGROUND)
        self.body.pack(fill="both", expand=True, padx=10, pady=10)
        for row in layout:
            row_frame = tk.Frame(self.body, bg=BACKGROUND)
            grows = _contains_type(row, ("table", "multiline"))
            row_frame.pack(fill="both" if grows else "x", expand=grows, pady=2)
            self._build_row(row_frame, row)

        self.top.update_idletasks()
        self._fit_to_screen(size)
        self.top.withdraw()

    def _fit_to_screen(self, size=None):
        self.top.update_idletasks()
        requested_w = self.top.winfo_reqwidth()
        requested_h = self.top.winfo_reqheight()
        if size is None:
            width = self.top.winfo_width()
            height = self.top.winfo_height()
            if width <= 1 or height <= 1:
                width = requested_w
                height = requested_h
        else:
            width = max(size[0], requested_w)
            height = max(size[1], requested_h)
        screen_w = self.top.winfo_screenwidth()
        screen_h = self.top.winfo_screenheight()
        width = min(width, max(480, screen_w - 80))
        height = min(height, max(160, screen_h - 120))
        x = max(0, (screen_w - width) // 2)
        y = max(0, (screen_h - height) // 2)
        self.top.geometry(f"{width}x{height}+{x}+{y}")
        self.top.minsize(min(width, 480), min(height, 120))

    def __getitem__(self, key):
        return self.elements[key]

    def read(self):
        if self._closed:
            return None, {}
        try:
            self.top.wait_variable(self._tick)
        except tk.TclError:
            return None, {}
        if self._closed:
            return None, {}
        return self._pending, self._values()

    def hide(self):
        if not self._closed:
            self.top.withdraw()

    def un_hide(self):
        if self._closed:
            return
        self.top.deiconify()
        self._fit_to_screen()
        self.top.lift()
        self.top.focus_force()

    def close(self):
        self._on_close()

    def _on_close(self):
        if self._closed:
            return
        self._closed = True
        self._pending = None
        try:
            self._tick.set(self._tick.get() + 1)
            self.top.destroy()
        except tk.TclError:
            pass

    def _emit(self, name):
        if self._closed:
            return
        self.top.after(0, lambda: self._fire(name))

    def _fire(self, name):
        if self._closed:
            return
        self._pending = name
        self._tick.set(self._tick.get() + 1)

    def _values(self):
        skipped = ("table", "button")
        return {key: element.get() for key, element in self.elements.items() if element.kind not in skipped}

    def _build_row(self, parent, row):
        for item in row:
            if item is None:
                continue
            if isinstance(item, list):
                box = tk.Frame(parent, bg=BACKGROUND)
                box.pack(side="left", fill="x", expand=True)
                if item and isinstance(item[0], list):
                    for nested in item:
                        line = tk.Frame(box, bg=BACKGROUND)
                        line.pack(fill="x", pady=1)
                        self._build_row(line, nested)
                else:
                    self._build_row(box, item)
                continue
            self._place(parent, item)

    def _place(self, parent, item):
        kind = item["type"]
        if kind == "text":
            label = tk.Label(
                parent,
                text=item["text"],
                bg=item["background"] or BACKGROUND,
                fg=FOREGROUND,
                anchor="w",
                justify="left",
                width=item["width"] or 0,
            )
            label.pack(side="left", padx=(0, 6))
            return
        if kind == "button":
            btn = ttk.Button(parent, text=item["text"], style="App.TButton", command=lambda key=item["key"]: self._emit(key))
            if item["disabled"]:
                btn.configure(state="disabled")
            btn.pack(side="left", padx=3)
            self.elements[item["key"]] = Element("button", btn)
            return
        if kind == "input":
            entry = tk.Entry(
                parent,
                width=item["width"],
                bg=FIELD,
                fg=FOREGROUND,
                insertbackground=FOREGROUND,
                relief="flat",
            )
            if item["default"] != "":
                entry.insert(0, item["default"])
            entry.pack(side="left", fill="x" if item["expand"] else "none", expand=item["expand"], padx=3, ipady=3)
            if item["enable_events"]:
                entry.bind("<KeyRelease>", lambda _event, key=item["key"]: self._emit(key))
            self.elements[item["key"]] = Element("input", entry)
            return
        if kind == "file":
            target = self._previous_input()
            ttk.Button(
                parent,
                text="Browse",
                style="App.TButton",
                command=lambda target=target, item=item: self._browse_file(target, item),
            ).pack(side="left", padx=3)
            return
        if kind == "folder":
            target = self._previous_input()
            ttk.Button(
                parent,
                text="Browse",
                style="App.TButton",
                command=lambda target=target: self._browse_folder(target),
            ).pack(side="left", padx=3)
            return
        if kind == "checkbox":
            variable = tk.BooleanVar(master=self.top, value=item["default"])
            check = ttk.Checkbutton(
                parent,
                text=item["text"],
                style="App.TCheckbutton",
                variable=variable,
                command=(lambda key=item["key"]: self._emit(key)) if item["enable_events"] else None,
            )
            if item["disabled"]:
                check.configure(state="disabled")
            check.pack(side="left", padx=6)
            self.elements[item["key"]] = Element("checkbox", check, variable)
            return
        if kind == "multiline":
            box = tk.Text(
                parent,
                width=item["width"],
                height=item["height"],
                bg=FIELD,
                fg=FOREGROUND,
                insertbackground=FOREGROUND,
                relief="flat",
            )
            if item["default"]:
                box.insert("1.0", item["default"])
            box.pack(fill="both", expand=True, pady=4)
            self.elements[item["key"]] = Element("multiline", box)
            return
        if kind == "listbox":
            variable = tk.StringVar(master=self.top, value=item["default"][0] if item["default"] else "")
            listed = tk.Listbox(
                parent,
                height=item["height"],
                width=item["width"],
                bg=FIELD,
                fg=FOREGROUND,
                exportselection=False,
                relief="flat",
            )
            for entry in item["items"]:
                listed.insert("end", entry)
            if item["default"]:
                try:
                    listed.selection_set(item["items"].index(item["default"][0]))
                except ValueError:
                    pass
            listed.pack(side="left", padx=3)
            listed.bind("<<ListboxSelect>>", lambda _event, key=item["key"]: self._emit(key))
            self.elements[item["key"]] = Element("listbox", listed, variable)
            return
        if kind == "table":
            holder = tk.Frame(parent, bg=BACKGROUND)
            columns = [f"c{index}" for index in range(len(item["headings"]))]
            tree = ttk.Treeview(holder, columns=columns, show="headings", height=item["height"])
            for column, heading in zip(columns, item["headings"]):
                tree.heading(column, text=heading)
                tree.column(column, width=max(80, len(heading) * 9), anchor="center", stretch=True)
            y_scroll = ttk.Scrollbar(holder, orient="vertical", command=tree.yview)
            x_scroll = ttk.Scrollbar(holder, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
            tree.grid(row=0, column=0, sticky="nsew")
            y_scroll.grid(row=0, column=1, sticky="ns")
            x_scroll.grid(row=1, column=0, sticky="ew")
            holder.rowconfigure(0, weight=1)
            holder.columnconfigure(0, weight=1)
            if item["visible"]:
                holder.pack(fill="both", expand=True, pady=4)
            self.elements[item["key"]] = Element("table", tree, holder=holder)

    def _previous_input(self):
        inputs = [element for element in self.elements.values() if element.kind == "input"]
        if not inputs:
            raise RuntimeError("Browse needs an input field before it")
        return inputs[-1]

    def _browse_file(self, target, item):
        initial = item["initial_folder"]
        if not initial or not os.path.isdir(initial):
            initial = None
        chosen = filedialog.askopenfilename(
            parent=self.top,
            initialdir=initial,
            filetypes=_file_types(item["file_types"]),
        )
        if not chosen:
            return
        target.update(value=chosen)
        key = self._key_for(target)
        if key:
            self._emit(key)

    def _browse_folder(self, target):
        current = target.get()
        initial = current if current and os.path.isdir(current) else None
        chosen = filedialog.askdirectory(parent=self.top, initialdir=initial)
        if not chosen:
            return
        target.update(value=chosen)
        key = self._key_for(target)
        if key:
            self._emit(key)

    def _key_for(self, target):
        for key, element in self.elements.items():
            if element is target:
                return key
        return None


def _file_types(file_types):
    merged = {}
    order = []
    for description, pattern in file_types:
        if description not in merged:
            order.append(description)
            merged[description] = []
        if pattern not in merged[description]:
            merged[description].append(pattern)
    normalized = [(description, " ".join(merged[description])) for description in order]
    normalized.append(("All files", "*.*"))
    return normalized
