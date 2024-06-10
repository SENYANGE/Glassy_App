screen_helper="""
#screen manager
ScreenManager:
    SplashScreen:
    LoginScreen:
    
#defining screens
<SplashScreen>:
    name:'SplashScreen'
    text:'Login'
    MDLable:
        text:'Login'
        halign:'center'
   
    
<LoginScreen>:
    name:'LoginScreen'
    text:'Glassy Login'
    theme_text_color:'Error'
    pos_hint:{'center-x':0.5,'center-y':0.5}



"""