# readme

## Abstract

1. [執行](#執行)

## 執行

有虛擬環境.venv，建議切換到.venv環境內跑

- 初次下載後建立 .venv 虛擬環境管理依賴:

    ```bash
    python -m venv .venv
    ```

- 啟動虛擬環境:

  - Mac/Linux/Git bash

    ```bash
    source .venv/Scripts/activate
    ```

- 依照 requirements.txt 下載依賴包:

    ```bash
    pip install -r requirements.txt
    ```

- 更新 requirements.txt:

    ```bash
    pip freeze > requirements.txt
    ```
