import { router } from '@kit.ArkUI'

@Entry
@Component
struct RegisterPage {
  @State currentStep: number = 1 // 当前步骤 1-3
  @State phoneNumber: string = ''
  @State verificationCode: string = ''
  @State password: string = ''
  @State confirmPassword: string = ''
  @State isAgreed: boolean = false
  @State countdown: number = 0
  @State passwordStrength: number = 0 // 密码强度 0-3

  // 倒计时定时器
  private timer: number = -1

  build() {
    Column() {
      // 顶部进度条
      Column() {
        Row() {
          Text('注册')
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .fontColor('#333333')
        }
        .width('100%')
        .height(50)
        .justifyContent(FlexAlign.Center)
        .margin({ top: 20, bottom: 20 })

        // 进度条
        Row() {
          ForEach([1, 2, 3], (step: number) => {
            Row() {
              Circle({ width: 20, height: 20 })
                .fill(this.currentStep >= step ? '#FFD700' : '#E0E0E0')

              if (step < 3) {
                Divider()
                  .color(this.currentStep > step ? '#FFD700' : '#E0E0E0')
                  .height(2)
                  .layoutWeight(1)
                  .margin({ left: 10, right: 10 })
              }
            }
          })
        }
        .width('80%')
        .margin({ bottom: 10 })

        Row() {
          Text('手机验证')
            .fontSize(12)
            .fontColor(this.currentStep >= 1 ? '#FFD700' : '#999999')
            .width('33%')
            .textAlign(TextAlign.Center)

          Text('设置密码')
            .fontSize(12)
            .fontColor(this.currentStep >= 2 ? '#FFD700' : '#999999')
            .width('33%')
            .textAlign(TextAlign.Center)

          Text('完成')
            .fontSize(12)
            .fontColor(this.currentStep >= 3 ? '#FFD700' : '#999999')
            .width('33%')
            .textAlign(TextAlign.Center)
        }
        .width('100%')
        .margin({ bottom: 40 })
      }
      .width('100%')
      .padding({ left: 30, right: 30 })

      // 表单区域
      Column() {
        if (this.currentStep === 1) {
          // 第一步：手机验证
          this.buildPhoneVerificationStep()
        } else if (this.currentStep === 2) {
          // 第二步：设置密码
          this.buildPasswordStep()
        } else {
          // 第三步：完成
          this.buildCompleteStep()
        }
      }
      .width('100%')
      .padding({ left: 30, right: 30 })
      .layoutWeight(1)

      // 安全提示
      Row() {
        Image($r('app.media.lock_icon'))
          .width(16)
          .height(16)
          .margin({ right: 8 })

        Text('LoCal采用银行级加密保护您的信息')
          .fontSize(12)
          .fontColor('#999999')
      }
      .justifyContent(FlexAlign.Center)
      .margin({ bottom: 40 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Color.White)
  }

  @Builder
  buildPhoneVerificationStep() {
    Column() {
      // 手机号输入
      Row() {
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
      }
      .width('100%')
      .height(50)
      .padding({ left: 15, right: 15 })
      .backgroundColor('#F8F8F8')
      .borderRadius(8)
      .border({ width: 1, color: '#E0E0E0' })
      .margin({ bottom: 20 })

      // 验证码输入
      Row() {
        TextInput({ placeholder: '请输入验证码', text: this.verificationCode })
          .fontSize(16)
          .fontColor('#333333')
          .backgroundColor(Color.Transparent)
          .border({ width: 0 })
          .layoutWeight(1)
          .onChange((value: string) => {
            this.verificationCode = value
          })

        Button(this.countdown > 0 ? `${this.countdown}s` : '获取验证码')
          .fontSize(14)
          .fontColor(this.countdown > 0 ? '#999999' : '#FFD700')
          .backgroundColor(Color.Transparent)
          .border({ width: 1, color: this.countdown > 0 ? '#E0E0E0' : '#FFD700' })
          .borderRadius(4)
          .height(32)
          .enabled(this.countdown === 0)
          .onClick(() => {
            this.startCountdown()
          })
      }
      .width('100%')
      .height(50)
      .padding({ left: 15, right: 15 })
      .backgroundColor('#F8F8F8')
      .borderRadius(8)
      .border({ width: 1, color: '#E0E0E0' })
      .margin({ bottom: 30 })

      // 协议勾选
      Row() {
        Checkbox()
          .select(this.isAgreed)
          .selectedColor('#FFD700')
          .onChange((value: boolean) => {
            this.isAgreed = value
          })
          .margin({ right: 8 })

        Text('我已阅读并同意')
          .fontSize(14)
          .fontColor('#333333')

        Text('《用户协议》')
          .fontSize(14)
          .fontColor('#FFD700')
          .onClick(() => {
            console.log('User agreement clicked')
          })
      }
      .margin({ bottom: 30 })

      // 下一步按钮
      Button('下一步')
        .width('100%')
        .height(50)
        .backgroundColor('#FFD700')
        .fontColor(Color.Black)
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .borderRadius(8)
        .enabled(this.isAgreed && this.phoneNumber.length > 0 && this.verificationCode.length > 0)
        .onClick(() => {
          this.currentStep = 2
        })
    }
    .alignItems(HorizontalAlign.Start)
  }

  @Builder
  buildPasswordStep() {
    Column() {
      // 密码输入
      Column() {
        TextInput({ placeholder: '请设置密码（8-20位）', text: this.password })
          .fontSize(16)
          .fontColor('#333333')
          .backgroundColor('#F8F8F8')
          .borderRadius(8)
          .border({ width: 1, color: '#E0E0E0' })
          .height(50)
          .type(InputType.Password)
          .onChange((value: string) => {
            this.password = value
            this.calculatePasswordStrength(value)
          })
          .margin({ bottom: 10 })

        // 密码强度提示
        Row() {
          Text('密码强度：')
            .fontSize(12)
            .fontColor('#999999')

          Row() {
            ForEach([1, 2, 3], (level: number) => {
              Divider()
                .color(this.passwordStrength >= level ?
                  (this.passwordStrength === 1 ? '#FF4444' :
                    this.passwordStrength === 2 ? '#FF8800' : '#00CC00') : '#E0E0E0')
                .height(4)
                .width(30)
                .margin({ right: 5 })
            })
          }
          .margin({ left: 10 })
        }
        .margin({ bottom: 20 })
      }
      .width('100%')

      // 确认密码
      TextInput({ placeholder: '请再次输入密码', text: this.confirmPassword })
        .fontSize(16)
        .fontColor('#333333')
        .backgroundColor('#F8F8F8')
        .borderRadius(8)
        .border({ width: 1, color: '#E0E0E0' })
        .height(50)
        .type(InputType.Password)
        .onChange((value: string) => {
          this.confirmPassword = value
        })
        .margin({ bottom: 40 })

      // 完成注册按钮
      Button('完成注册')
        .width('100%')
        .height(50)
        .backgroundColor('#FFD700')
        .fontColor(Color.Black)
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .borderRadius(8)
        .enabled(this.password.length >= 8 && this.password === this.confirmPassword)
        .onClick(() => {
          this.currentStep = 3
        })
    }
    .alignItems(HorizontalAlign.Start)
  }

  @Builder
  buildCompleteStep() {
    Column() {
      Image($r('app.media.success_icon'))
        .width(80)
        .height(80)
        .margin({ bottom: 30 })

      Text('注册成功！')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .fontColor('#333333')
        .margin({ bottom: 10 })

      Text('欢迎加入LoCal大家庭')
        .fontSize(16)
        .fontColor('#666666')
        .margin({ bottom: 60 })

      Button('立即体验')
        .width('100%')
        .height(50)
        .backgroundColor('#FFD700')
        .fontColor(Color.Black)
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .borderRadius(8)
        .onClick(() => {
          // 跳转到主页
          router.replaceUrl({url:'pages/main'});
          console.log('Start experience clicked')
        })
    }
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
    .height('100%')
  }

  // 开始倒计时
  startCountdown() {
    this.countdown = 60
    this.timer = setInterval(() => {
      this.countdown--
      if (this.countdown <= 0) {
        clearInterval(this.timer)
        this.countdown = 0
      }
    }, 1000)
  }

  // 计算密码强度
  calculatePasswordStrength(password: string) {
    let strength = 0
    if (password.length >= 8) strength++
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++
    if (/\d/.test(password) && /[!@#$%^&*]/.test(password)) strength++
    this.passwordStrength = strength
  }

  aboutToDisappear() {
    if (this.timer !== -1) {
      clearInterval(this.timer)
    }
  }
}