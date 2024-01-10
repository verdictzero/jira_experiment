@echo off
pushd \\network_share_path
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {python .\jira_api_test_gui_module_w700.py}"
popd
pause