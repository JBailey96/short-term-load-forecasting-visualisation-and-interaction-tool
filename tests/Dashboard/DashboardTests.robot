*** Settings ***
Documentation
Resource          ../dependencies.txt

*** Test Cases ***
Open dashboard and see a graph
    Open Browser  http://127.0.0.1:8050/  browser=gc
    Element Should Be Visible           id=load-data
    Element Should Contain              class=gtitle      Load over time
    Element Should Contain              class=g-xtitle    Day
    Element Should Contain              class=g-ytitle    Load
    Close Browser
