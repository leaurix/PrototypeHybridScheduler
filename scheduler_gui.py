"""
Hybrid Scheduler — Tkinter GUI
"""

import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

# ── PyInstaller bundle path fix ──────────────────────────────────────────────
if getattr(sys, 'frozen', False):
    _BASE = sys._MEIPASS
    if _BASE not in sys.path:
        sys.path.insert(0, _BASE)
else:
    _BASE = os.path.dirname(os.path.abspath(__file__))

# ── timeslot label mapping ──────────────────────────────────────────────────
TIMESLOT_LABELS = {
    "TSMon_AM":  "Monday    07:30 – 09:00",
    "TSMon_PM":  "Monday    13:00 – 14:30",
    "TSTue_AM":  "Tuesday   07:30 – 09:00",
    "TSTue_PM":  "Tuesday   13:00 – 14:30",
    "TSWed_AM":  "Wednesday 07:30 – 09:00",
    "TSWed_PM":  "Wednesday 13:00 – 14:30",
    "TSThu_AM":  "Thursday  07:30 – 09:00",
    "TSThu_PM":  "Thursday  13:00 – 14:30",
    "TSFri_AM":  "Friday    07:30 – 09:00",
    "TSFri_PM":  "Friday    13:00 – 14:30",
}

def friendly_timeslot(ts):
    return TIMESLOT_LABELS.get(ts, ts)

# ── colour palette ───────────────────────────────────────────────────────────
BG          = "#0f1117"
PANEL       = "#1a1d27"
CARD        = "#22263a"
ACCENT      = "#4f8ef7"
ACCENT2     = "#7c6ef7"
SUCCESS     = "#3ecf8e"
WARNING     = "#f5a623"
TEXT        = "#e8eaf6"
SUBTEXT     = "#8892b0"
BORDER      = "#2d3250"
RED         = "#f07178"

FONT_H1     = ("Segoe UI", 20, "bold")
FONT_H2     = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_MONO   = ("Consolas", 9)

# ── helper widgets ───────────────────────────────────────────────────────────
class ScrollableFrame(tk.Frame):
    def __init__(self, parent, **kw):
        outer = tk.Frame(parent, bg=kw.get("bg", PANEL))
        outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, bg=kw.get("bg", PANEL), highlightthickness=0)
        sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        super().__init__(canvas, bg=kw.get("bg", PANEL))
        self.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))


def make_label(parent, text, font=FONT_BODY, fg=TEXT, bg=PANEL, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)


def make_button(parent, text, command, bg=ACCENT, fg="white", **kw):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg, relief="flat", cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        activebackground=ACCENT2, activeforeground="white",
        padx=14, pady=6, **kw
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT2))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def card_frame(parent, bg=CARD, padx=12, pady=12):
    f = tk.Frame(parent, bg=bg, padx=padx, pady=pady)
    f.configure(relief="flat", bd=0)
    return f


# ────────────────────────────────────────────────────────────────────────────
#  Main Application
# ────────────────────────────────────────────────────────────────────────────
class SchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hybrid Scheduler — FGASP")
        self.geometry("1200x760")
        self.minsize(900, 600)
        self.configure(bg=BG)

        self._data_dir = tk.StringVar(value=os.path.join(_BASE, "dummy_dataset"))
        self._ga_pop    = tk.IntVar(value=10)
        self._ga_gen    = tk.IntVar(value=5)
        self._ga_mut    = tk.DoubleVar(value=0.10)
        self._alns_iter = tk.IntVar(value=20)

        self._dataset   = None
        self._output    = None
        self._schedule_df = None

        self._build_styles()
        self._build_ui()

    # ── styles ───────────────────────────────────────────────────────────────
    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook",        background=BG,    borderwidth=0)
        style.configure("TNotebook.Tab",    background=PANEL, foreground=SUBTEXT,
                        font=("Segoe UI", 10, "bold"), padding=[18, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", CARD)],
                  foreground=[("selected", TEXT)])
        style.configure("Treeview",         background=CARD,  foreground=TEXT,
                        fieldbackground=CARD, rowheight=26, font=FONT_BODY)
        style.configure("Treeview.Heading", background=PANEL, foreground=ACCENT,
                        font=("Segoe UI", 9, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", ACCENT)])
        style.configure("TScrollbar", background=PANEL, troughcolor=BG)
        style.configure("TProgressbar", troughcolor=PANEL, background=ACCENT, thickness=6)
        style.configure("TCombobox",    fieldbackground=CARD, background=CARD,
                        foreground=TEXT, selectbackground=ACCENT)

    # ── layout ───────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── top bar ─────────────────────────────────────────────────────────
        top = tk.Frame(self, bg=PANEL, pady=10, padx=20)
        top.pack(fill="x")
        tk.Label(top, text="⚙", font=("Segoe UI", 22), bg=PANEL, fg=ACCENT).pack(side="left")
        tk.Label(top, text="  Hybrid Scheduler", font=FONT_H1, bg=PANEL, fg=TEXT).pack(side="left")
        tk.Label(top, text="FGASP · GA · ALNS · CSP", font=FONT_SMALL,
                 bg=PANEL, fg=SUBTEXT).pack(side="left", padx=14, pady=6)

        # ── notebook ─────────────────────────────────────────────────────────
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        self._tab_config   = tk.Frame(nb, bg=BG)
        self._tab_run      = tk.Frame(nb, bg=BG)
        self._tab_schedule = tk.Frame(nb, bg=BG)
        self._tab_stats    = tk.Frame(nb, bg=BG)

        nb.add(self._tab_config,   text="  ⚙ Configuration  ")
        nb.add(self._tab_run,      text="  ▶ Run  ")
        nb.add(self._tab_schedule, text="  📋 Schedule  ")
        nb.add(self._tab_stats,    text="  📊 Statistics  ")

        self._build_config_tab()
        self._build_run_tab()
        self._build_schedule_tab()
        self._build_stats_tab()

    # ── CONFIG TAB ───────────────────────────────────────────────────────────
    def _build_config_tab(self):
        p = self._tab_config
        tk.Frame(p, bg=BG, height=16).pack()

        # Data directory
        sec = card_frame(p)
        sec.pack(fill="x", padx=30, pady=6)
        make_label(sec, "Dataset Directory", font=FONT_H2, bg=CARD).pack(anchor="w")
        make_label(sec, "Folder containing students.csv, courses.csv, rooms.csv, instructors.csv, timeslots.csv",
                   fg=SUBTEXT, bg=CARD, font=FONT_SMALL).pack(anchor="w", pady=(2, 8))
        row = tk.Frame(sec, bg=CARD)
        row.pack(fill="x")
        entry = tk.Entry(row, textvariable=self._data_dir, bg=PANEL, fg=TEXT,
                         insertbackground=TEXT, font=FONT_BODY, relief="flat",
                         bd=0, highlightthickness=1, highlightbackground=BORDER)
        entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 8))
        make_button(row, "Browse…", self._browse_dir, bg=ACCENT2).pack(side="left")

        # GA params
        sec2 = card_frame(p)
        sec2.pack(fill="x", padx=30, pady=6)
        make_label(sec2, "Genetic Algorithm", font=FONT_H2, bg=CARD).pack(anchor="w", pady=(0, 10))
        self._param_row(sec2, "Population Size",  self._ga_pop,  1, 200)
        self._param_row(sec2, "Generations",       self._ga_gen,  1, 100)
        self._param_row(sec2, "Mutation Rate",     self._ga_mut,  0.01, 0.50, is_float=True)

        # ALNS params
        sec3 = card_frame(p)
        sec3.pack(fill="x", padx=30, pady=6)
        make_label(sec3, "ALNS", font=FONT_H2, bg=CARD).pack(anchor="w", pady=(0, 10))
        self._param_row(sec3, "Iterations", self._alns_iter, 1, 500)

    def _param_row(self, parent, label, var, lo, hi, is_float=False):
        row = tk.Frame(parent, bg=CARD)
        row.pack(fill="x", pady=3)
        make_label(row, label, bg=CARD, fg=SUBTEXT, width=18, anchor="w").pack(side="left")
        if is_float:
            sb = tk.Spinbox(row, from_=lo, to=hi, increment=0.01,
                            textvariable=var, width=8,
                            bg=PANEL, fg=TEXT, insertbackground=TEXT,
                            buttonbackground=PANEL, relief="flat", font=FONT_BODY,
                            format="%.2f")
        else:
            sb = tk.Spinbox(row, from_=lo, to=hi, increment=1,
                            textvariable=var, width=8,
                            bg=PANEL, fg=TEXT, insertbackground=TEXT,
                            buttonbackground=PANEL, relief="flat", font=FONT_BODY)
        sb.pack(side="left", padx=8, ipady=4)

    def _browse_dir(self):
        d = filedialog.askdirectory(initialdir=self._data_dir.get())
        if d:
            self._data_dir.set(d)

    # ── RUN TAB ──────────────────────────────────────────────────────────────
    def _build_run_tab(self):
        p = self._tab_run
        tk.Frame(p, bg=BG, height=16).pack()

        top = card_frame(p)
        top.pack(fill="x", padx=30, pady=6)
        self._run_btn = make_button(top, "▶  Run Scheduler", self._start_run, bg=SUCCESS, fg="black")
        self._run_btn.pack(side="left")
        self._stop_btn = make_button(top, "■  Clear", self._clear_log, bg=PANEL)
        self._stop_btn.pack(side="left", padx=8)

        # progress
        prog_card = card_frame(p)
        prog_card.pack(fill="x", padx=30, pady=6)
        make_label(prog_card, "Progress", font=FONT_H2, bg=CARD).pack(anchor="w")
        self._status_var = tk.StringVar(value="Ready")
        make_label(prog_card, "", bg=CARD, fg=SUBTEXT,
                   textvariable=self._status_var).pack(anchor="w", pady=(2, 6))
        self._progress = ttk.Progressbar(prog_card, mode="indeterminate", style="TProgressbar")
        self._progress.pack(fill="x")

        # log
        log_card = card_frame(p, padx=0, pady=0)
        log_card.pack(fill="both", expand=True, padx=30, pady=6)
        make_label(log_card, "  Output Log", font=FONT_H2, bg=CARD,
                   anchor="w").pack(fill="x", padx=12, pady=8)
        self._log = tk.Text(log_card, bg="#0b0e1a", fg=TEXT, font=FONT_MONO,
                            relief="flat", bd=0, state="disabled",
                            insertbackground=TEXT, wrap="word")
        sb = ttk.Scrollbar(log_card, command=self._log.yview)
        self._log.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._log.pack(fill="both", expand=True, padx=2, pady=2)

        # colour tags
        self._log.tag_config("hdr",     foreground=ACCENT,   font=("Consolas", 9, "bold"))
        self._log.tag_config("ok",      foreground=SUCCESS)
        self._log.tag_config("warn",    foreground=WARNING)
        self._log.tag_config("err",     foreground=RED)
        self._log.tag_config("sub",     foreground=SUBTEXT)

    def _log_write(self, text, tag=""):
        self._log.configure(state="normal")
        self._log.insert("end", text, tag)
        self._log.see("end")
        self._log.configure(state="disabled")

    def _clear_log(self):
        self._log.configure(state="normal")
        self._log.delete("1.0", "end")
        self._log.configure(state="disabled")
        self._status_var.set("Ready")

    def _start_run(self):
        self._run_btn.config(state="disabled")
        self._clear_log()
        self._progress.start(12)
        self._status_var.set("Running…")
        t = threading.Thread(target=self._run_pipeline, daemon=True)
        t.start()

    def _run_pipeline(self):
        try:
            from hybrid_scheduler.utils.dataset_loader import load_dataset
            from hybrid_scheduler.fgasp.pipeline import HybridSchedulingPipeline

            data_dir = self._data_dir.get()

            self._log_write("═" * 56 + "\n", "hdr")
            self._log_write(" HYBRID SCHEDULER — FGASP PIPELINE\n", "hdr")
            self._log_write("═" * 56 + "\n\n", "hdr")

            self._log_write("[1/5] Loading dataset…\n", "sub")
            self.after(0, lambda: self._status_var.set("Loading dataset…"))

            ds = load_dataset(
                os.path.join(data_dir, "students.csv"),
                os.path.join(data_dir, "courses.csv"),
                os.path.join(data_dir, "rooms.csv"),
                os.path.join(data_dir, "instructors.csv"),
                os.path.join(data_dir, "timeslots.csv"),
            )
            self._dataset = ds

            self._log_write(f"      Students   : {len(ds.students)}\n")
            self._log_write(f"      Courses    : {len(ds.courses)}\n")
            self._log_write(f"      Timeslots  : {len(ds.timeslots)}\n")
            self._log_write(f"      Instructors: {len(ds.instructors)}\n")
            self._log_write(f"      Rooms      : {len(ds.rooms)}\n\n", "ok")

            self._log_write("[2/5] Building pipeline…\n", "sub")
            self.after(0, lambda: self._status_var.set("Building pipeline…"))

            pipeline = HybridSchedulingPipeline(
                ds,
                ga_population_size=self._ga_pop.get(),
                ga_generations=self._ga_gen.get(),
                ga_mutation_rate=self._ga_mut.get(),
                alns_iterations=self._alns_iter.get(),
            )

            self._log_write(f"      GA  — pop={self._ga_pop.get()}  gen={self._ga_gen.get()}  mut={self._ga_mut.get():.2f}\n")
            self._log_write(f"      ALNS — iter={self._alns_iter.get()}\n\n")

            self._log_write("[3/5] Running GA + ALNS + FGASP…\n", "sub")
            self.after(0, lambda: self._status_var.set("Running optimisation…"))

            t0 = time.time()
            output = pipeline.run()
            elapsed = time.time() - t0
            self._output = output

            ga_res   = output["ga_result"]
            alns_res = output["alns_result"]
            best_res = output["best_result"]
            decision = output["decision"]["chosen"]
            best_sch = output["best_solution"]

            self._log_write(f"\n[4/5] Optimisation complete in {elapsed:.3f}s\n\n", "ok")

            self._log_write("─" * 40 + "\n", "sub")
            self._log_write(" RESULTS\n", "hdr")
            self._log_write("─" * 40 + "\n", "sub")
            self._log_write(f"  GA result   : {ga_res}\n")
            self._log_write(f"  ALNS result : {alns_res}\n")
            self._log_write(f"  FGASP chose : {decision}\n", "warn")
            self._log_write(f"  Best result : {best_res}\n\n", "ok")

            # Build schedule dataframe
            rows = []
            for (s, c, t), v in best_sch.items():
                if v == 1:
                    rows.append({"student_id": s, "course_id": c, "timeslot": t})
            df = pd.DataFrame(rows)
            df["time_label"] = df["timeslot"].map(lambda x: friendly_timeslot(x))
            self._schedule_df = df

            self._log_write("[5/5] Building schedule view…\n", "sub")
            self.after(0, self._populate_schedule)
            self.after(0, self._populate_stats)

            self._log_write("\n✔  Done.\n", "ok")
            self.after(0, lambda: self._status_var.set(f"Done — {elapsed:.2f}s"))

        except Exception as ex:
            import traceback
            self._log_write(f"\n[ERROR] {ex}\n", "err")
            self._log_write(traceback.format_exc(), "err")
            self.after(0, lambda: self._status_var.set("Error — see log"))
        finally:
            self.after(0, self._progress.stop)
            self.after(0, lambda: self._run_btn.config(state="normal"))

    # ── SCHEDULE TAB ─────────────────────────────────────────────────────────
    def _build_schedule_tab(self):
        p = self._tab_schedule
        tk.Frame(p, bg=BG, height=16).pack()

        # filter bar
        bar = card_frame(p)
        bar.pack(fill="x", padx=30, pady=6)
        make_label(bar, "Filter", font=FONT_H2, bg=CARD).pack(anchor="w", pady=(0, 8))

        row = tk.Frame(bar, bg=CARD)
        row.pack(fill="x")

        make_label(row, "Student:", bg=CARD, fg=SUBTEXT).pack(side="left")
        self._filter_student = tk.StringVar(value="All")
        self._combo_student  = ttk.Combobox(row, textvariable=self._filter_student,
                                            width=10, state="readonly")
        self._combo_student.pack(side="left", padx=(4, 16))

        make_label(row, "Course:", bg=CARD, fg=SUBTEXT).pack(side="left")
        self._filter_course = tk.StringVar(value="All")
        self._combo_course  = ttk.Combobox(row, textvariable=self._filter_course,
                                           width=10, state="readonly")
        self._combo_course.pack(side="left", padx=(4, 16))

        make_label(row, "Day:", bg=CARD, fg=SUBTEXT).pack(side="left")
        self._filter_day = tk.StringVar(value="All")
        self._combo_day  = ttk.Combobox(row, textvariable=self._filter_day,
                                        values=["All", "Monday", "Tuesday", "Wednesday",
                                                "Thursday", "Friday"],
                                        width=12, state="readonly")
        self._combo_day.pack(side="left", padx=(4, 16))

        make_button(row, "Apply", self._apply_filter, bg=ACCENT).pack(side="left", padx=4)
        make_button(row, "Export CSV", self._export_csv, bg=ACCENT2).pack(side="right", padx=4)

        # treeview
        tree_card = card_frame(p, padx=0, pady=0)
        tree_card.pack(fill="both", expand=True, padx=30, pady=6)

        cols = ("student_id", "course_id", "day", "time")
        self._tree = ttk.Treeview(tree_card, columns=cols, show="headings")
        self._tree.heading("student_id", text="Student")
        self._tree.heading("course_id",  text="Course")
        self._tree.heading("day",        text="Day")
        self._tree.heading("time",       text="Time")
        self._tree.column("student_id",  width=110, anchor="center")
        self._tree.column("course_id",   width=110, anchor="center")
        self._tree.column("day",         width=120, anchor="center")
        self._tree.column("time",        width=160, anchor="center")

        vsb = ttk.Scrollbar(tree_card, orient="vertical",   command=self._tree.yview)
        hsb = ttk.Scrollbar(tree_card, orient="horizontal",  command=self._tree.xview)
        self._tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self._tree.pack(fill="both", expand=True)

        # alternating row colours
        self._tree.tag_configure("odd",  background="#1e2235")
        self._tree.tag_configure("even", background=CARD)

        self._count_var = tk.StringVar(value="No schedule loaded yet.")
        make_label(p, "", textvariable=self._count_var, fg=SUBTEXT,
                   bg=BG, font=FONT_SMALL).pack(anchor="e", padx=32, pady=2)

    def _populate_schedule(self):
        df = self._schedule_df
        if df is None or df.empty:
            return

        # update combos
        students = ["All"] + sorted(df["student_id"].unique())
        courses  = ["All"] + sorted(df["course_id"].unique())
        self._combo_student.config(values=students)
        self._combo_course.config(values=courses)
        self._filter_student.set("All")
        self._filter_course.set("All")
        self._filter_day.set("All")

        self._fill_tree(df)

    def _apply_filter(self):
        if self._schedule_df is None:
            return
        df = self._schedule_df.copy()
        if self._filter_student.get() != "All":
            df = df[df["student_id"] == self._filter_student.get()]
        if self._filter_course.get() != "All":
            df = df[df["course_id"] == self._filter_course.get()]
        if self._filter_day.get() != "All":
            df = df[df["time_label"].str.startswith(self._filter_day.get())]
        self._fill_tree(df)

    def _fill_tree(self, df):
        for row in self._tree.get_children():
            self._tree.delete(row)

        df_sorted = df.sort_values(["student_id", "timeslot"])
        for i, (_, r) in enumerate(df_sorted.iterrows()):
            label  = r["time_label"]
            parts  = label.split()
            day    = parts[0].strip() if parts else ""
            trange = " ".join(parts[1:]).strip() if len(parts) > 1 else label
            tag    = "odd" if i % 2 else "even"
            self._tree.insert("", "end",
                              values=(r["student_id"], r["course_id"], day, trange),
                              tags=(tag,))

        self._count_var.set(f"{len(df_sorted):,} assignments shown")

    def _export_csv(self):
        if self._schedule_df is None:
            messagebox.showwarning("No data", "Run the scheduler first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="output_schedule.csv",
        )
        if path:
            out = self._schedule_df[["student_id", "course_id", "timeslot", "time_label"]]
            out.to_csv(path, index=False)
            messagebox.showinfo("Exported", f"Saved to:\n{path}")

    # ── STATS TAB ────────────────────────────────────────────────────────────
    def _build_stats_tab(self):
        p = self._tab_stats
        tk.Frame(p, bg=BG, height=16).pack()

        self._stats_frame = tk.Frame(p, bg=BG)
        self._stats_frame.pack(fill="both", expand=True, padx=30, pady=6)

        make_label(self._stats_frame,
                   "Run the scheduler to see statistics.",
                   fg=SUBTEXT, bg=BG, font=FONT_H2).pack(pady=40)

    def _populate_stats(self):
        # clear
        for w in self._stats_frame.winfo_children():
            w.destroy()

        df = self._schedule_df
        if df is None or df.empty:
            return

        # ── summary cards ────────────────────────────────────────────────────
        summary_row = tk.Frame(self._stats_frame, bg=BG)
        summary_row.pack(fill="x", pady=(0, 12))

        totals = [
            ("Total Assignments", len(df), ACCENT),
            ("Students",          df["student_id"].nunique(), SUCCESS),
            ("Courses",           df["course_id"].nunique(), WARNING),
            ("Timeslots Used",    df["timeslot"].nunique(), ACCENT2),
        ]
        for label, val, col in totals:
            c = card_frame(summary_row, padx=20, pady=14)
            c.pack(side="left", fill="both", expand=True, padx=6)
            tk.Label(c, text=str(val), font=("Segoe UI", 28, "bold"),
                     bg=CARD, fg=col).pack()
            make_label(c, label, fg=SUBTEXT, bg=CARD, font=FONT_SMALL).pack()

        # ── course load ───────────────────────────────────────────────────────
        course_row = tk.Frame(self._stats_frame, bg=BG)
        course_row.pack(fill="x", pady=6)

        cc = card_frame(course_row, padx=16, pady=12)
        cc.pack(side="left", fill="both", expand=True, padx=6)
        make_label(cc, "Enrollments per Course", font=FONT_H2, bg=CARD).pack(anchor="w")
        enroll = df.groupby("course_id")["student_id"].count().reset_index()
        enroll.columns = ["Course", "Students"]
        self._mini_table(cc, enroll)

        # ── timeslot usage ────────────────────────────────────────────────────
        tc = card_frame(course_row, padx=16, pady=12)
        tc.pack(side="left", fill="both", expand=True, padx=6)
        make_label(tc, "Assignments per Timeslot", font=FONT_H2, bg=CARD).pack(anchor="w")
        ts_usage = (df.groupby("timeslot")["student_id"]
                    .count()
                    .reset_index()
                    .rename(columns={"student_id": "Assignments"}))
        ts_usage["Timeslot"] = ts_usage["timeslot"].map(friendly_timeslot)
        ts_usage = ts_usage[["Timeslot", "Assignments"]].sort_values("Assignments", ascending=False)
        self._mini_table(tc, ts_usage)

        # ── per-student load distribution ─────────────────────────────────────
        bc = card_frame(self._stats_frame, padx=16, pady=12)
        bc.pack(fill="x", padx=6, pady=6)
        make_label(bc, "Courses per Student (first 20)", font=FONT_H2, bg=CARD).pack(anchor="w")
        per_stu = (df.groupby("student_id")["course_id"]
                   .count()
                   .reset_index()
                   .rename(columns={"course_id": "Courses"})
                   .head(20))
        self._bar_chart(bc, per_stu, "student_id", "Courses", color=ACCENT)

    def _mini_table(self, parent, df):
        cols = list(df.columns)
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=min(8, len(df)))
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=140, anchor="center")
        for i, (_, row) in enumerate(df.iterrows()):
            tag = "odd" if i % 2 else "even"
            tree.insert("", "end", values=list(row), tags=(tag,))
        tree.tag_configure("odd",  background="#1e2235")
        tree.tag_configure("even", background=CARD)
        tree.pack(fill="x", pady=(6, 0))

    def _bar_chart(self, parent, df, x_col, y_col, color=ACCENT):
        import tkinter.font as tkfont
        max_val = df[y_col].max() if len(df) else 1
        BAR_H = 22
        LABEL_W = 70
        BAR_AREA = 340
        PAD = 4

        canvas = tk.Canvas(parent, bg=CARD, highlightthickness=0,
                           height=(BAR_H + PAD) * len(df) + 10)
        canvas.pack(fill="x", pady=(8, 0))

        for i, (_, row) in enumerate(df.iterrows()):
            y0 = 5 + i * (BAR_H + PAD)
            y1 = y0 + BAR_H
            label  = str(row[x_col])
            val    = row[y_col]
            bar_w  = int((val / max_val) * BAR_AREA)

            canvas.create_text(LABEL_W - 4, (y0 + y1) // 2,
                               text=label, anchor="e", fill=SUBTEXT,
                               font=("Segoe UI", 8))
            if bar_w > 0:
                canvas.create_rectangle(LABEL_W, y0, LABEL_W + bar_w, y1,
                                        fill=color, outline="")
            canvas.create_text(LABEL_W + bar_w + 4, (y0 + y1) // 2,
                               text=str(val), anchor="w", fill=TEXT,
                               font=("Segoe UI", 8))


# ── entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = SchedulerApp()
    app.mainloop()
