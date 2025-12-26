# ============================================================
# Tool Name : Output_Nulls
# Version   : 1.0.0
# Author    : Nitin Kashyap
# Software  : Houdini 19+ / 20 / 21
# Description:
#   Professional Output_Nulls creator with UI
#   Designed for VFX / Rig / FX pipelines
# ============================================================




import hou


try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PySide2 import QtCore, QtWidgets


def getHoudiniWindow():
    return hou.ui.mainQtWindow()


class OutputNulls(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # ---------------- Window ----------------
        self.setWindowTitle("Output / Output_Nulls")
        self.resize(800, 200)

        central = QtWidgets.QWidget(self)
        layout = QtWidgets.QGridLayout(central)
        layout.setSpacing(6)
        layout.setContentsMargins(6, 6, 6, 6)

        # ---------------- Name Input ----------------
        self.nameInput = QtWidgets.QLineEdit()
        self.nameInput.setPlaceholderText("Optional suffix")
        layout.addWidget(self.nameInput, 0, 0, 1, 7)
        self.nameInput.returnPressed.connect(self.trigger_default_action)

        # ---------------- Buttons ----------------
        self.buttons = {
            "OUT": QtWidgets.QPushButton("OUT"),
            "OUT_RENDER": QtWidgets.QPushButton("OUT_RENDER"),
            "OUT_GEO": QtWidgets.QPushButton("OUT_GEO"),
            "OUT_PTS": QtWidgets.QPushButton("OUT_PTS"),
            "OUT_VOLUME": QtWidgets.QPushButton("OUT_VOLUME"),
            "OBJ_MERGE": QtWidgets.QPushButton("OBJ_MERGE"),
            "QUIT": QtWidgets.QPushButton("QUIT"),
        }

        for col, btn in enumerate(self.buttons.values()):
            btn.setFixedHeight(34)
            layout.addWidget(btn, 1, col)

        self.setCentralWidget(central)

        # ---------------- UI COLORS / STYLISH BUTTONS ----------------
        styles = {
            "OUT":        "#E53935",
            "OUT_RENDER": "#FB8C00",
            "OUT_GEO":    "#8E24AA",
            "OUT_PTS":    "#00ACC1",
            "OUT_VOLUME": "#43A047",
            "OBJ_MERGE":  "#1E88E5",
            "QUIT":       "#757575",
        }

        for key, btn in self.buttons.items():
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {styles[key]};
                    color: white;
                    border-radius: 6px;
                    border: 1px solid #222;
                    font-weight: bold;
                    font-size: 13px;
                    padding: 6px 12px;
                    box-shadow: 2px 2px 6px rgba(0,0,0,0.4);
                }}
                QPushButton:hover {{
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ffffff33, stop:1 {styles[key]}
                    );
                    color: white;
                }}
                QPushButton:pressed {{
                    background-color: #333333;
                    color: white;
                }}
            """)

        # ---------------- Signals ----------------
        for name, btn in self.buttons.items():
            if name == "QUIT":
                btn.clicked.connect(self.close)
            elif name == "OBJ_MERGE":
                btn.clicked.connect(self.create_object_merge)
            else:
                btn.clicked.connect(self.create_output_null)

        # Houdini parenting
        self.setParent(getHoudiniWindow(), QtCore.Qt.Window)

    # ---------------- OUT NULL ----------------
    def create_output_null(self):
        nodes = hou.selectedNodes()
        if not nodes:
            hou.ui.displayMessage("Select at least one node.")
            return

        label = self.sender().text() if self.sender() else "OUT"

        colors = {
            "OUT": hou.Color((0.83, 0.18, 0.18)),
            "OUT_RENDER": hou.Color((0.90, 0.32, 0.00)),
            "OUT_GEO": hou.Color((0.48, 0.12, 0.64)),
            "OUT_PTS": hou.Color((0.00, 0.59, 0.65)),
            "OUT_VOLUME": hou.Color((0.18, 0.49, 0.20)),
        }

        for node in nodes:
            parent = node.parent()
            null = parent.createNode("null")
            null.setInput(0, node)
            null.setPosition(node.position() + hou.Vector2(0, -1.5))

            suffix = self.nameInput.text().strip() or node.name()
            null.setName(f"{label}_{suffix}", unique_name=True)
            null.setColor(colors.get(label, hou.Color((0.8, 0.8, 0.8))))

        parent.layoutChildren()
        self.close()

    # ---------------- OBJECT MERGE ----------------
    def create_object_merge(self):
        nodes = hou.selectedNodes()
        if not nodes:
            hou.ui.displayMessage("Select at least one node.")
            return

        for node in nodes:
            parent = node.parent()
            obj_merge = parent.createNode("object_merge")
            obj_merge.parm("objpath1").set(node.path())
            obj_merge.parm("xformtype").set(1)
            obj_merge.setPosition(node.position() + hou.Vector2(0, -1.5))
            obj_merge.setColor(hou.Color((0.10, 0.45, 0.85)))

            suffix = self.nameInput.text().strip() or node.name()
            obj_merge.setName(f"OBJ_{suffix}", unique_name=True)

        parent.layoutChildren()
        self.close()

    # ---------------- Trigger Default Action ----------------
    def trigger_default_action(self):
        default_button = self.buttons.get("OUT")
        if default_button:
            default_button.click()


# ---------------- Launch ----------------
try:
    outputWidget.close()
except:
    pass

outputWidget = OutputNulls()
outputWidget.setWindowFlags(
    QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
)
outputWidget.setStyleSheet("""
    QMainWindow {
        background-color: rgb(50,50,50);
    }
""")
# outputWidget.show()





try:
    outputWidget.close()
except:
    pass

outputWidget = OutputNulls()
outputWidget.show()