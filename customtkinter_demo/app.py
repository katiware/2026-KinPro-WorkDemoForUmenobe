"""
KinPro 2026: CustomTkinter Desktop Studio
新入生向けデスクトップアプリケーション制作デモ
"""

import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# ─────────────────────────────────────────────────────────────────────────────
# アプリケーションの初期設定
# ─────────────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("Dark")          # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")     # "blue", "dark-blue", "green"


class KinProDesktopApp(ctk.CTk):
    """KinPro 2026 作品制作向け CustomTkinter デスクトップアプリ."""

    def __init__(self):
        super().__init__()

        # ウィンドウの基本設定
        self.title("KinPro 2026 Desktop Studio (CustomTkinter)")
        self.geometry("1080x680")
        self.minsize(860, 520)

        # グリッドレイアウト (1行 × 2列: 左サイドバー / 右メインエリア)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 内部状態
        self.project_data = [
            {"id": 1, "name": "2Dアクションゲーム企画", "status": "進行中", "progress": 0.75, "tag": "Godot"},
            {"id": 2, "name": "部費管理ダッシュボード", "status": "完了", "progress": 1.0, "tag": "Streamlit"},
            {"id": 3, "name": "クリエイティブツールGUI", "status": "制作中", "progress": 0.40, "tag": "CustomTkinter"},
        ]

        # UIコンポーネントの作成
        self._create_sidebar()
        self._create_main_frames()

        # デフォルト画面を表示
        self._select_frame_by_name("dashboard")

    # ─────────────────────────────────────────────────────────────────────────
    # サイドバー
    # ─────────────────────────────────────────────────────────────────────────
    def _create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # ロゴ・タイトル
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="✨ KinPro Studio",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(24, 16))

        # ナビゲーションボタン
        self.nav_btn_dashboard = ctk.CTkButton(
            self.sidebar_frame,
            text="📊 ダッシュボード",
            font=ctk.CTkFont(size=14),
            height=40,
            command=lambda: self._select_frame_by_name("dashboard")
        )
        self.nav_btn_dashboard.grid(row=1, column=0, padx=16, pady=6, sticky="ew")

        self.nav_btn_editor = ctk.CTkButton(
            self.sidebar_frame,
            text="📝 エディタ & ツール",
            font=ctk.CTkFont(size=14),
            height=40,
            command=lambda: self._select_frame_by_name("editor")
        )
        self.nav_btn_editor.grid(row=2, column=0, padx=16, pady=6, sticky="ew")

        self.nav_btn_settings = ctk.CTkButton(
            self.sidebar_frame,
            text="⚙️ 設定 & テーマ",
            font=ctk.CTkFont(size=14),
            height=40,
            command=lambda: self._select_frame_by_name("settings")
        )
        self.nav_btn_settings.grid(row=3, column=0, padx=16, pady=6, sticky="ew")

        # サイドバー下部（外観モード切り替え）
        self.appearance_label = ctk.CTkLabel(self.sidebar_frame, text="外観モード:", anchor="w")
        self.appearance_label.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="w")
        self.appearance_mode_option = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["Dark", "Light", "System"],
            command=self._change_appearance_mode
        )
        self.appearance_mode_option.grid(row=7, column=0, padx=20, pady=(4, 10), sticky="ew")

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI拡大率:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(4, 0), sticky="w")
        self.scaling_option = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "100%", "120%"],
            command=self._change_scaling
        )
        self.scaling_option.set("100%")
        self.scaling_option.grid(row=9, column=0, padx=20, pady=(4, 20), sticky="ew")

    # ─────────────────────────────────────────────────────────────────────────
    # 各種メインフレームの構築
    # ─────────────────────────────────────────────────────────────────────────
    def _create_main_frames(self):
        # 1. ダッシュボード画面
        self.frame_dashboard = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self._build_dashboard_ui()

        # 2. エディタ＆ツール画面
        self.frame_editor = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self._build_editor_ui()

        # 3. 設定画面
        self.frame_settings = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self._build_settings_ui()

    def _select_frame_by_name(self, name: str):
        """サイドバーボタンのアクティブ色制御とフレーム表示切り替え."""
        buttons = {
            "dashboard": self.nav_btn_dashboard,
            "editor": self.nav_btn_editor,
            "settings": self.nav_btn_settings,
        }
        for btn_name, btn in buttons.items():
            if btn_name == name:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")

        # フレーム切り替え
        frames = {
            "dashboard": self.frame_dashboard,
            "editor": self.frame_editor,
            "settings": self.frame_settings,
        }
        for f_name, frame in frames.items():
            if f_name == name:
                frame.grid(row=0, column=1, sticky="nsew", padx=24, pady=24)
            else:
                frame.grid_forget()

    # ─────────────────────────────────────────────────────────────────────────
    # 1. ダッシュボード UI
    # ─────────────────────────────────────────────────────────────────────────
    def _build_dashboard_ui(self):
        self.frame_dashboard.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame_dashboard.grid_rowconfigure(2, weight=1)

        # ページヘッダー
        header = ctk.CTkLabel(
            self.frame_dashboard,
            text="📊 KinPro 2026 作品制作プロジェクト管理",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w"
        )
        header.grid(row=0, column=0, columnspan=3, pady=(0, 16), sticky="w")

        # KPIカード 3つ
        kpis = [
            ("📁 進行中の作品数", "3 件", "#38bdf8"),
            ("🎯 平均進捗率", "71.6 %", "#22c55e"),
            ("⏱️ うめの辺祭まで", "残り 65 日", "#f59e0b"),
        ]
        for i, (title, val, color) in enumerate(kpis):
            card = ctk.CTkFrame(self.frame_dashboard, corner_radius=12)
            card.grid(row=1, column=i, padx=8, pady=8, sticky="nsew")
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=13), text_color="gray70").grid(row=0, column=0, padx=12, pady=(12, 4))
            ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=24, weight="bold"), text_color=color).grid(row=1, column=0, padx=12, pady=(0, 12))

        # プロジェクト一覧テーブル（スクロール可能フレーム）
        list_label = ctk.CTkLabel(
            self.frame_dashboard,
            text="📋 登録中の制作プロジェクト",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        list_label.grid(row=2, column=0, columnspan=3, pady=(16, 8), sticky="w")

        self.scroll_projects = ctk.CTkScrollableFrame(self.frame_dashboard, height=260)
        self.scroll_projects.grid(row=3, column=0, columnspan=3, sticky="nsew")
        self.scroll_projects.grid_columnconfigure(1, weight=1)

        self._render_project_list()

        # アクションボタンエリア
        btn_frame = ctk.CTkFrame(self.frame_dashboard, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=3, pady=(16, 0), sticky="ew")

        add_btn = ctk.CTkButton(
            btn_frame,
            text="➕ 新規プロジェクト追加",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._dialog_add_project
        )
        add_btn.pack(side="left", padx=6)

        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 リフレッシュ",
            fg_color="gray30",
            hover_color="gray40",
            command=self._render_project_list
        )
        refresh_btn.pack(side="left", padx=6)

    def _render_project_list(self):
        """プロジェクト一覧の再描画."""
        for widget in self.scroll_projects.winfo_children():
            widget.destroy()

        for idx, item in enumerate(self.project_data):
            row_frame = ctk.CTkFrame(self.scroll_projects, corner_radius=8)
            row_frame.pack(fill="x", padx=4, pady=4)
            row_frame.grid_columnconfigure(1, weight=1)

            # タグバッジ
            tag_label = ctk.CTkLabel(
                row_frame,
                text=f"[{item['tag']}]",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#818cf8",
                width=100,
                anchor="w"
            )
            tag_label.grid(row=0, column=0, padx=12, pady=10)

            # プロジェクト名
            name_label = ctk.CTkLabel(
                row_frame,
                text=item["name"],
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            name_label.grid(row=0, column=1, padx=8, pady=10, sticky="w")

            # プログレスバー
            p_bar = ctk.CTkProgressBar(row_frame, width=150)
            p_bar.set(item["progress"])
            p_bar.grid(row=0, column=2, padx=12, pady=10)

            p_val = ctk.CTkLabel(row_frame, text=f"{int(item['progress'] * 100)}%", width=45)
            p_val.grid(row=0, column=3, padx=4, pady=10)

    def _dialog_add_project(self):
        """プロジェクト追加ダイアログ."""
        dialog = ctk.CTkInputDialog(text="新しいプロジェクト名を入力してください:", title="新規プロジェクト追加")
        name = dialog.get_input()
        if name and name.strip():
            self.project_data.append({
                "id": len(self.project_data) + 1,
                "name": name.strip(),
                "status": "企画中",
                "progress": 0.1,
                "tag": "新規作品"
            })
            self._render_project_list()
            messagebox.showinfo("成功", f"プロジェクト「{name.strip()}」を追加しました！")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. エディタ & ツール UI
    # ─────────────────────────────────────────────────────────────────────────
    def _build_editor_ui(self):
        self.frame_editor.grid_rowconfigure(1, weight=1)
        self.frame_editor.grid_columnconfigure(0, weight=1)

        # ヘッダー
        header = ctk.CTkLabel(
            self.frame_editor,
            text="📝 クリエイティブ・テキスト & スクリプトツール",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w"
        )
        header.grid(row=0, column=0, pady=(0, 12), sticky="w")

        # テキストエリア
        self.textbox = ctk.CTkTextbox(self.frame_editor, font=ctk.CTkFont(family="Consolas", size=13))
        self.textbox.grid(row=1, column=0, sticky="nsew", pady=6)
        self.textbox.insert("1.0", "# KinPro 2026 アイデアメモ / スクリプト下書き\n\ndef hello_kinpro():\n    print('Hello, Umenobe Festival 2026!')\n")

        # ツールバー
        tools_frame = ctk.CTkFrame(self.frame_editor)
        tools_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        btn_open = ctk.CTkButton(tools_frame, text="📂 ファイルを開く", width=120, command=self._open_file)
        btn_open.pack(side="left", padx=8, pady=8)

        btn_save = ctk.CTkButton(tools_frame, text="💾 保存する", width=100, command=self._save_file)
        btn_save.pack(side="left", padx=8, pady=8)

        btn_count = ctk.CTkButton(tools_frame, text="📊 文字数カウント", width=120, fg_color="gray30", command=self._count_stats)
        btn_count.pack(side="left", padx=8, pady=8)

        btn_clear = ctk.CTkButton(tools_frame, text="🗑️ クリア", width=80, fg_color="#ef4444", hover_color="#dc2626", command=self._clear_text)
        btn_clear.pack(side="right", padx=8, pady=8)

    def _open_file(self):
        fpath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt;*.py;*.gd;*.md"), ("All files", "*.*")])
        if fpath:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", content)

    def _save_file(self):
        fpath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("Python files", "*.py")])
        if fpath:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(self.textbox.get("1.0", "end-1c"))
            messagebox.showinfo("保存完了", f"ファイルを保存しました:\n{fpath}")

    def _count_stats(self):
        text = self.textbox.get("1.0", "end-1c")
        chars = len(text)
        lines = len(text.splitlines())
        words = len(text.split())
        messagebox.showinfo("テキスト統計", f"文字数: {chars:,} 文字\n行数: {lines:,} 行\n単語数: {words:,} 語")

    def _clear_text(self):
        if messagebox.askyesno("確認", "エディタの内容を全消去しますか？"):
            self.textbox.delete("1.0", "end")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. 設定 UI
    # ─────────────────────────────────────────────────────────────────────────
    def _build_settings_ui(self):
        self.frame_settings.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            self.frame_settings,
            text="⚙️ アプリケーション設定",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w"
        )
        header.grid(row=0, column=0, pady=(0, 20), sticky="w")

        # テーマカラー選択
        theme_card = ctk.CTkFrame(self.frame_settings)
        theme_card.grid(row=1, column=0, sticky="ew", pady=8, padx=4)

        ctk.CTkLabel(theme_card, text="カラーテーマ:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=16, pady=16)
        color_theme_menu = ctk.CTkOptionMenu(theme_card, values=["blue", "dark-blue", "green"], command=self._change_color_theme)
        color_theme_menu.pack(side="right", padx=16, pady=16)

        # 通知・サウンドスイッチ
        switch_card = ctk.CTkFrame(self.frame_settings)
        switch_card.grid(row=2, column=0, sticky="ew", pady=8, padx=4)

        switch_notify = ctk.CTkSwitch(switch_card, text="自動バックアップ機能を有効化")
        switch_notify.select()
        switch_notify.pack(side="left", padx=16, pady=16)

        # アプリ情報カード
        about_card = ctk.CTkFrame(self.frame_settings)
        about_card.grid(row=3, column=0, sticky="ew", pady=16, padx=4)

        ctk.CTkLabel(about_card, text="ℹ️ KinPro 2026 Desktop Studio について", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=16, pady=(16, 4))
        desc = (
            "CustomTkinter を使用して構築されたモダンなデスクトップGUIアプリケーションです。\n"
            "新入生がPythonでネイティブなデスクトップツールやユーティリティを制作する際のテンプレートとして活用できます。\n"
            "PyInstaller を使用することで、単一の .exe 実行ファイルに変換して配布することも可能です。"
        )
        ctk.CTkLabel(about_card, text=desc, justify="left", text_color="gray70").pack(anchor="w", padx=16, pady=(0, 16))

    # ─────────────────────────────────────────────────────────────────────────
    # イベントハンドラ
    # ─────────────────────────────────────────────────────────────────────────
    def _change_appearance_mode(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)

    def _change_scaling(self, new_scaling: str):
        val = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(val)

    def _change_color_theme(self, new_theme: str):
        ctk.set_default_color_theme(new_theme)
        messagebox.showinfo("テーマ変更", "カラーテーマを適用しました（アプリ再起動時に完全に反映されます）。")


if __name__ == "__main__":
    app = KinProDesktopApp()
    app.mainloop()
