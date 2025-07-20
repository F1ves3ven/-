import { router } from '@kit.ArkUI'

// LoCal启动页面组件
@Entry
@Component
struct SplashScreen {
  @State logoScale: number = 0.8
  @State logoOpacity: number = 0
  @State sloganOpacity: number = 0
  @State loadingTextOpacity: number = 0
  @State particlePositions: number[] = []

  // 动画定时器
  private animationTimer: number = -1
  private particleTimer: number = -1

  aboutToAppear() {
    this.initParticles()
    this.startSplashAnimation()
  }

  build() {
    Stack() {
      // 背景层 - 动态黄色粒子背景
      this.buildAnimatedBackground()

      // 城市轮廓剪影层
      this.buildCitySilhouette()

      // 主视觉内容层
      this.buildMainContent()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#FFD000')
  }

  @Builder
  buildAnimatedBackground() {
    // 流动的黄色粒子背景
    Stack() {
      ForEach(Array.from<void, number>({ length: 15 }, (_, i) => i), (index: number) => {
        Circle({ width: 6 + index % 3 * 2, height: 6 + index % 3 * 2 })
          .fill('#FFE55C')
          .opacity(0.4 + (index % 3) * 0.2)
          .position({
            x: (index * 50 + (this.particlePositions[index] || 0)) % 350,
            y: (index * 30 + Math.sin(index) * 40) % 700
          })
      }, (index: number) => index.toString())
    }
    .width('100%')
    .height('100%')
  }

  @Builder
  buildCitySilhouette() {
    // 底层城市轮廓剪影
    Row() {
      // 模拟城市建筑轮廓
      ForEach([60, 120, 80, 150, 100, 180, 90, 140], (height: number, index: number) => {
        Rect()
          .width(35)
          .height(height)
          .fill('#E6B800')
          .opacity(0.15)
          .margin({ right: index < 7 ? 3 : 0 })
      }, (height: number, index: number) => `building_${index}`)
    }
    .width('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(VerticalAlign.Bottom)
    .position({ x: 0, y: '75%' })
  }

  @Builder
  buildMainContent() {
    Column() {
      // Logo动画区域
      Stack() {
        // 黄色光晕效果
        Circle({ width: 180, height: 180 })
          .fill('#FFE55C')
          .opacity(this.sloganOpacity > 0 ? 0.2 : 0)
          .scale({ x: this.sloganOpacity > 0 ? 1.1 : 0.9 })
          .animation({
            duration: 2000,
            curve: Curve.EaseInOut,
            iterations: -1,
            playMode: PlayMode.Alternate
          })

        // 黑色圆形背景
        Image($r('app.media.LoCal_icon'))
          .width(180)
          .height(180)
          .borderRadius(65.2)
          .objectFit(ImageFit.Contain)
          .opacity(this.logoOpacity)
          .scale({ x: this.logoScale, y: this.logoScale })
          .animation({
            duration: 800,
            delay: 400,
            curve: Curve.EaseOut
          })
      }
      .width(180)
      .height(180)
      .margin({ bottom: 50 })

      // 标语
      Column() {
        Text('Local Life, Delivered Now')
          .fontSize(18)
          .fontColor('#333333')
          .fontWeight(FontWeight.Medium)
          .opacity(this.sloganOpacity)
          .animation({
            duration: 600,
            delay: 1200,
            curve: Curve.EaseOut
          })

        Text('本地生活，即刻送达')
          .fontSize(14)
          .fontColor('#666666')
          .margin({ top: 8 })
          .opacity(this.sloganOpacity)
          .animation({
            duration: 600,
            delay: 1400,
            curve: Curve.EaseOut
          })
      }
      .margin({ bottom: 80 })

      // 加载提示文字
      Text('正在为您准备精彩内容...')
        .fontSize(18)
        .fontColor('#666666')
        .opacity(this.loadingTextOpacity)
        .animation({
          duration: 600,
          delay: 1800,
          curve: Curve.EaseOut
        })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }

  // 初始化粒子位置
  initParticles() {
    this.particlePositions = Array.from<void, number>({ length: 15 }, () => Math.random() * 100)
    this.startParticleAnimation()
  }

  // 开始粒子动画
  startParticleAnimation() {
    this.particleTimer = setInterval(() => {
      this.particlePositions = this.particlePositions.map((pos, index) => {
        return (pos + 0.5 + index * 0.1) % 300
      })
    }, 100)
  }

  // 启动页面主动画序列
  startSplashAnimation() {
    // 第一阶段：Logo出现动画 (0-0.8秒)
    setTimeout(() => {
      this.logoScale = 1.0
      this.logoOpacity = 1.0
    }, 300)

    // 第二阶段：标语出现 (1-1.8秒)
    setTimeout(() => {
      this.sloganOpacity = 1.0
    }, 1200)

    // 第三阶段：加载文字出现 (1.8秒后)
    setTimeout(() => {
      this.loadingTextOpacity = 1.0
    }, 1800)

    // 自动跳转到主页面 (3秒后)
    setTimeout(() => {
      this.navigateToMainPage()
    }, 3000)
  }

  // 跳转到主页面
  navigateToMainPage() {
    // 淡出动画
    this.logoOpacity = 0
    this.sloganOpacity = 0
    this.loadingTextOpacity = 0

    // 跳转逻辑
    setTimeout(() => {
      console.log('Navigate to main page')
      // 这里添加路由跳转代码
      router.replaceUrl({ url: 'pages/Start' })
    }, 500)
  }

  aboutToDisappear() {
    // 清理定时器
    if (this.animationTimer !== -1) {
      clearTimeout(this.animationTimer)
    }
    if (this.particleTimer !== -1) {
      clearInterval(this.particleTimer)
    }
  }
}