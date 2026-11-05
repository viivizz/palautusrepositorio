*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  maija
    Set Password  maija123
    Set Password Confirmation  maija123
    Click  button >> text=Register
    Get Title  ==  Welcome to Ohtu Application!

Register With Too Short Username And Valid Password
    Set Username  ma
    Set Password  maija123
    Set Password Confirmation  maija123
    Click  button >> text=Register

Register With Valid Username And Too Short Password
    Set Username  maija
    Set Password  maija12
    Set Password Confirmation  maija12
    Click  button >> text=Register

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click  button >> text=Register

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page

Set Password Confirmation
    [Arguments]  ${password}
    Fill Secret  id=password_confirmation  $password