import { router } from '@kit.ArkUI'

// 登录页面组件
@Entry
@Component
struct StartPage {
  @State phoneNumber: string = ''
  @State password: string = ''
  @State isPasswordVisible: boolean = false
  @State isLoginMode: boolean = true // true: 密码登录, false: 验证码登录
  @State isFocused: boolean = false

  build() {
    Column() {
      // 顶部Logo区域
      Column() {
        Row() {
          //Text('LoCal')
          Image($r('app.media.LoCal_icon'))
            .width(100)
            .height(100)
            .borderRadius(36.2)

        }
        //.width(100)
        //.height(100)
        //.backgroundColor('#FFD700')
        //.borderRadius(40)
        //.justifyContent(FlexAlign.Center)
        .margin({ top: 60, bottom: 20 })

        Text('本地生活，即刻送达')
          .fontSize(16)
          .fontColor('#666666')
          .margin({ bottom: 60 })
      }
      .width('100%')
      .alignItems(HorizontalAlign.Center)

      // 主体表单区域
      Column() {
        // 手机号输入框
        Row() {
          Image($r('app.media.phone_icon'))
            .width(20)
            .height(20)
            .margin({ right: 10 })

          Text('+86')
            .fontSize(16)
            .fontColor('#333333')
            .margin({ right: 10 })

          Divider()
            .vertical(true)
            .height(20)
            .color('#E0E0E0')
            .margin({ right: 10 })

          TextInput({ placeholder: '请输入手机号', text: this.phoneNumber })
            .fontSize(16)
            .fontColor('#333333')
            .backgroundColor(Color.Transparent)
            .border({ width: 0 })
            .layoutWeight(1)
            .onChange((value: string) => {
              this.phoneNumber = value
            })
            .onFocus(() => {
              this.isFocused = true
            })
            .onBlur(() => {
              this.isFocused = false
            })
        }
        .width('100%')
        .height(50)
        .padding({ left: 15, right: 15 })
        .backgroundColor('#F8F8F8')
        .borderRadius(8)
        .border({
          width: this.isFocused ? 2 : 1,
          color: this.isFocused ? '#FFD700' : '#E0E0E0'
        })
        .margin({ bottom: 20 })

        // 密码输入框（登录模式）或验证码输入框
        if (this.isLoginMode) {
          Row() {
            Image($r('app.media.lock_icon'))
              .width(20)
              .height(20)
              .margin({ right: 10 })

            TextInput({
              placeholder: '请输入密码',
              text: this.password
            })
              .fontSize(16)
              .fontColor('#333333')
              .backgroundColor(Color.Transparent)
              .border({ width: 0 })
              .layoutWeight(1)
              .type(this.isPasswordVisible ? InputType.Normal : InputType.Password)
              .onChange((value: string) => {
                this.password = value
              })

              //Image(this.isPasswordVisible ? $r('app.media.eye_open_') : $r('app.media.eye_close_'))
              //.width(20)
              //.height(20)
              .onClick(() => {
                this.isPasswordVisible = !this.isPasswordVisible
              })
          }
          .width('100%')
          .height(50)
          .padding({ left: 15, right: 15 })
          .backgroundColor('#F8F8F8')
          .borderRadius(8)
          .border({ width: 1, color: '#E0E0E0' })
          .margin({ bottom: 20 })
        } else {
          // 验证码输入框
          Row() {
            TextInput({ placeholder: '请输入验证码' })
              .fontSize(16)
              .fontColor('#333333')
              .backgroundColor(Color.Transparent)
              .border({ width: 0 })
              .layoutWeight(1)

            Button('获取验证码')
              .fontSize(14)
              .fontColor('#FFD700')
              .backgroundColor(Color.Transparent)
              .border({ width: 1, color: '#FFD700' })
              .borderRadius(4)
              .height(32)
          }
          .width('100%')
          .height(50)
          .padding({ left: 15, right: 15 })
          .backgroundColor('#F8F8F8')
          .borderRadius(8)
          .border({ width: 1, color: '#E0E0E0' })
          .margin({ bottom: 20 })
        }

        // 登录按钮
        Button('登录')
          .width('100%')
          .height(50)
          .backgroundColor('#FFD700')
          .fontColor(Color.Black)
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
          .borderRadius(8)
          .margin({ bottom: 20 })
          .onClick(() => {
            // 登录逻辑
            router.replaceUrl({url:'pages/main'});
            console.log('Login clicked')
          })

        // 切换登录方式和忘记密码
        Row() {
          Text(this.isLoginMode ? '验证码登录' : '密码登录')
            .fontSize(14)
            .fontColor('#FFD700')
            .onClick(() => {
              this.isLoginMode = !this.isLoginMode
            })

          Blank()

          if (this.isLoginMode) {
            Text('忘记密码？')
              .fontSize(14)
              .fontColor('#999999')
              .onClick(() => {
                // 跳转到忘记密码页面
                console.log('Forgot password clicked')
              })
          }
        }
        .width('100%')
        .margin({ bottom: 40 })

        // 第三方登录分隔线
        Row() {
          Divider()
            .color('#E0E0E0')
            .layoutWeight(1)

          Text('其他登录方式')
            .fontSize(12)
            .fontColor('#999999')
            .margin({ left: 15, right: 15 })

          Divider()
            .color('#E0E0E0')
            .layoutWeight(1)
        }
        .width('100%')
        .margin({ bottom: 20 })

        // 第三方登录图标
        Row() {
          Image($r('app.media.wechat_icon'))
            .width(35)
            .height(35)
            .margin({ right: 30 })
            .onClick(() => {
              console.log('WeChat login clicked')
            })
          Image($r('app.media.qq_icon'))
            .width(35)
            .height(35)
            //.margin({ right: 30 })
            .onClick(() => {
              console.log('qq login clicked')
            })

        }
        .justifyContent(FlexAlign.Center)
        .margin({ bottom: 20 })

        // 未注册提示
        Text('未注册手机号自动注册')
          .fontSize(12)
          .fontColor('#999999')
          .margin({ bottom: 40 })
      }
      .width('100%')
      .padding({ left: 30, right: 30 })

      // 底部注册引导
      Row() {
        Text('新用户？')
          .fontSize(14)
          .fontColor('#333333')
          .margin({ right: 10 })

        Button('立即注册')
          .fontSize(14)
          .fontColor(Color.Black)
          .backgroundColor('#FFD700')
          .borderRadius(16)
          .height(32)
          .padding({ left: 20, right: 20 })
          .onClick(() => {
            // 跳转到注册页面
            router.replaceUrl({ url: 'pages/Register'});

            console.log('Register clicked')
          })
      }
      .justifyContent(FlexAlign.Center)
      .margin({ bottom: 40 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Color.White)
  }
}

// 注册页面组件
