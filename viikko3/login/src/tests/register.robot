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

Register With Password That Contains Digits
    Set Username  hannu
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click  button >> text=Register
    Get Title  ==  Welcome to Ohtu Application!

Register With Password That Contains A Special Character
    Set Username  sanna
    Set Password  kalle#abc
    Set Password Confirmation  kalle#abc
    Click  button >> text=Register
    Get Title  ==  Welcome to Ohtu Application!

Register With Password That Contains Only Letters
    Set Username  paula
    Set Password  kallekalle
    Set Password Confirmation  kallekalle
    Click  button >> text=Register
    Registration Should Fail With Message  Password must contain at least one non-letter character

Register With Password That Contains Only Uppercase Letters
    Set Username  miika
    Set Password  KalleKalle
    Set Password Confirmation  KalleKalle
    Click  button >> text=Register
    Registration Should Fail With Message  Password must contain at least one non-letter character

Register With Matching Password And Confirmation
    Set Username  liisa
    Set Password  liisa123
    Set Password Confirmation  liisa123
    Click  button >> text=Register
    Get Title  ==  Welcome to Ohtu Application!

Register With Different Password And Confirmation
    Set Username  pekka
    Set Password  pekka123
    Set Password Confirmation  pekka456
    Click  button >> text=Register
    Registration Should Fail With Message  Passwords do not match

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

Registration Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Get Text  body  *=  ${message}

Set Password Confirmation
    [Arguments]  ${password}
    Fill Secret  id=password_confirmation  $password