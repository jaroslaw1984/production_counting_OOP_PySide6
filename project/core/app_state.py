import pandas as pd


class AppState:
    def __init__(self):
        self.df: pd.DataFrame | None = None
        self.df_hydra = None
        self.hydra_path = None

        self.cfg = None
        self.machine_cfg = None

        self.table_frame = None

        self.last_report_text: str = ""
        self.last_report_data = None
        self.last_report_kind: str | None = None

        self.production_calculated: bool = False
