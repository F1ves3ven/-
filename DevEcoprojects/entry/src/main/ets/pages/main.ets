import { router } from '@kit.ArkUI'

@Builder
export function mainBuilder() {
  main();
}

@Component
struct main {
  pathStack: NavPathStack = new NavPathStack();

  build() {
    NavDestination() {
      MainTabPage()
    }
    .onReady((context: NavDestinationContext) => {
      this.pathStack = context.pathStack;
    })
  }
}

// 自定义间距组件
@Component
struct CustomSpacer {
  build() {
    Blank()
      .layoutWeight(1)
  }
}

// 数据接口
export interface Category {
  icon: Resource;
  title: string;
}

export interface Merchant {
  image: Resource;
  name: string;
  deliveryTime: string;
  rating: number;
  sales: string;
  minOrder: string;
  discount: string;
}

interface Message {
  id: number;
  title: string;
  content: string;
  time: string;
  isRead: boolean;
}

interface CartItem {
  id: number;
  name: string;
  price: number;
  count: number;
  image: Resource;
}

// 主Tab页面容器
@Entry
@Component
struct MainTabPage {
  @State currentIndex: number = 0;
  private tabsController: TabsController = new TabsController();

  build() {
    Column() {
      Tabs({ barPosition: BarPosition.End, controller: this.tabsController }) {
        TabContent() {
          HomePage()
        }
        .tabBar(this.TabBuilder(0, '首页', $r('app.media.Main_icon')))

        TabContent() {
          MessagePage()
        }
        .tabBar(this.TabBuilder(1, '消息', $r('app.media.Message_icon')))

        TabContent() {
          CartPage()
        }
        .tabBar(this.TabBuilder(2, '购物车', $r('app.media.Cart_icon')))

        TabContent() {
          MinePage()
        }
        .tabBar(this.TabBuilder(3, '我的', $r('app.media.Mine_icon')))
      }
      .onChange((index: number) => {
        this.currentIndex = index;
      })
      .animationDuration(300)
      .backgroundColor('#F5F5F5')
    }
    .width('100%')
    .height('100%')
  }

  @Builder
  TabBuilder(index: number, name: string, icon: Resource) {
    Column() {
      Image(icon)
        .width(24)
        .height(24)
        .fillColor(this.currentIndex === index ? '#FED700' : '#666666')

      Text(name)
        .fontSize(12)
        .margin({ top: 4 })
        .fontColor(this.currentIndex === index ? '#FED700' : '#666666')
    }
    .width('100%')
    .height(60)
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
    .backgroundColor('#FFFFFF')
  }
}

// 首页组件
@Component
struct HomePage {
  private categories: Category[] = [
    { icon: $r('app.media.Food_icon'), title: '美食' },
    { icon: $r('app.media.Snack_icon'), title: '快餐' },
    { icon: $r('app.media.Fruit_icon'), title: '水果' },
    { icon: $r('app.media.Dessert_icon'), title: '甜点' },
    { icon: $r('app.media.Supermarket_icon'), title: '超市' },
  ];

  private merchants: Merchant[] = [
    {
      image: $r('app.media.Merchant_Noodle_icon'),
      name: '老北京炸酱面',
      deliveryTime: '30分钟送达',
      rating: 4.5,
      sales: '月售2000+',
      minOrder: '起送20 | 配送5',
      discount: '新用户减10 | 会员折扣'
    },
    {
      image: $r('app.media.Merchant_Sushi_icon'),
      name: '寿司の物语',
      deliveryTime: '25分钟送达',
      rating: 4.7,
      sales: '月售1500+',
      minOrder: '起送30 | 配送8',
      discount: '满50减15 | 会员折扣'
    }
  ];

  // 星级评分组件
  @Builder
  RatingStars(rating: number) {
    Row() {
      ForEach(Array.from({length: 5}), (item: undefined, index: number) => {
        Image($r(rating >= index + 0.75 ? 'app.media.Star_icon' :
          rating >= index + 0.25 ? 'app.media.Star_icon_half' :
            'app.media.Star_icon_empty'))
          .width(12)
          .height(12)
          .margin({right: 2});
      })
    }
  }

  // 顶部导航栏
  @Builder
  TopBar() {
    Column() {
      Row() {
        // 左侧logo按钮
        Button() {
          Image($r('app.media.LoCal_icon'))
            .width(40)
            .height(40)
        }
        .type(ButtonType.Normal)
        .backgroundColor(Color.Transparent)
        .width(40)
        .height(40)

        // 中间标题
        CustomSpacer()

        Text('首页')
          .fontSize(18)
          .fontWeight(FontWeight.Medium)

        CustomSpacer()

        // 右侧占位保持对称
        Blank()
          .width(40)
      }
      .width('100%')
      .height(50)
      .padding(10)
      .backgroundColor('#FED700')
      .alignItems(VerticalAlign.Center)

      // 城市选择 + 搜索栏
      Column() {
        // 城市选择
        Row() {
          Image($r('app.media.Location_icon'))
            .width(16)
            .height(16)
            .margin({ right: 4 })
          Text('四川省成都市双流区')
            .fontSize(14)
            .fontColor('#000000')
          Image($r('app.media.Arrow_Down_icon'))
            .width(12)
            .height(12)
            .margin({ left: 4 })
        }
        .width('100%')
        .height(44)
        .padding({ left: 16 })
        .backgroundColor('#FED700')

        // 搜索栏
        Row() {
          TextInput({ placeholder: '搜索商家、美食' })
            .width('90%')
            .height(36)
            .backgroundColor('#FFFFFF')
            .borderRadius(18)
            .placeholderColor('#999999')
            .margin({ top: 8, bottom: 8 })
        }
        .justifyContent(FlexAlign.Center)
      }
    }
    .width('100%')
    .backgroundColor('#FED700')
  }

  build() {
    Column() {
      // 顶部导航栏
      this.TopBar()

      // 主内容区域
      Scroll() {
        Column() {
          // 广告横幅
          Image($r('app.media.Banner_Food_icon'))
            .width('100%')
            .height(120)
            .margin({ top: 8 })

          // 分类导航
          Column() {
            Scroll() {
              Row({ space: 12 }) {
                ForEach(this.categories, (category: Category) => {
                  Column({ space: 4 }) {
                    Image(category.icon)
                      .width(36)
                      .height(36)
                    Text(category.title)
                      .fontSize(12)
                      .fontColor('#333333')
                  }
                  .padding(8)
                  .backgroundColor('#FFFFFF')
                  .borderRadius(8)
                  .margin({ left: 8, right: 8 })
                })
              }
              .height(90)
              .padding({ top: 8, bottom: 8 })
            }
            .scrollable(ScrollDirection.Horizontal)
          }

          // 推荐商家
          Column() {
            Row() {
              Text('推荐商家')
                .fontSize(16)
                .fontWeight(FontWeight.Medium)
              Blank().layoutWeight(1)
              Text('综合排序')
                .fontSize(14)
                .fontColor('#999999')
            }
            .padding({ left: 16, right: 16 })
            .margin({ top: 16 })

            // 商家列表
            Column() {
              ForEach(this.merchants, (merchant: Merchant) => {
                Column({ space: 8 }) {
                  Image(merchant.image)
                    .width('100%')
                    .height(120)
                    .borderRadius(8)
                    .objectFit(ImageFit.Cover)

                  Column({ space: 6 }) {
                    Row() {
                      Text(merchant.name)
                        .fontSize(16)
                        .fontWeight(FontWeight.Medium)
                      Blank().layoutWeight(1)
                      Text(merchant.deliveryTime)
                        .fontSize(12)
                        .fontColor('#999999')
                    }

                    Row() {
                      this.RatingStars(merchant.rating)
                      Text(merchant.rating.toFixed(1))
                        .fontSize(12)
                        .fontColor('#FFA500')
                        .margin({ left: 4 })
                      Text(merchant.sales)
                        .fontSize(12)
                        .fontColor('#999999')
                        .margin({ left: 8 })
                    }

                    Row() {
                      Text(merchant.minOrder)
                        .fontSize(12)
                        .fontColor('#999999')
                      Blank().layoutWeight(1)
                      Text(merchant.discount)
                        .fontSize(12)
                        .fontColor('#FF5722')
                    }
                  }
                  .padding(8)
                }
                .width('100%')
                .backgroundColor('#FFFFFF')
                .borderRadius(8)
                .margin({ bottom: 12 })
                .padding(8)
                .gesture(
                  TapGesture()
                    .onAction(() => {
                      // 点击商家跳转到详情页
                      router.pushUrl({
                        url: 'pages/MerchantDetail',
                        params: { merchant: merchant }
                      });
                    })
                )
              })
            }
            .padding({ left: 12, right: 12 })
            .margin({ top: 8 })
          }
        }
      }
      .layoutWeight(1)
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
  }
}

// 消息页面
@Component
struct MessagePage {
  @State messages: Array<Message> = [
    { id: 1, title: '系统通知', content: '您的订单已送达，请及时取餐', time: '10:30', isRead: false },
    { id: 2, title: '优惠活动', content: '限时特惠！满50减15，仅限今日', time: '09:15', isRead: true },
    { id: 3, title: '配送提醒', content: '您的订单正在配送中，预计15分钟到达', time: '昨天', isRead: true },
  ];

  build() {
    Column() {
      // 顶部标题
      Row() {
        Text('消息中心')
          .fontSize(18)
          .fontWeight(FontWeight.Medium)
      }
      .width('100%')
      .height(50)
      .justifyContent(FlexAlign.Center)
      .backgroundColor('#FED700')

      // 消息列表
      List() {
        ForEach(this.messages, (message:Message) => {
          ListItem() {
            Row() {
              Column() {
                Row() {
                  Text(message.title)
                    .fontSize(16)
                    .fontWeight(FontWeight.Medium)
                  if (!message.isRead) {
                    Circle({ width: 8, height: 8 })
                      .fill('#FF5722')
                      .margin({ left: 8 })
                  }
                }
                .alignItems(VerticalAlign.Center)

                Text(message.content)
                  .fontSize(14)
                  .fontColor('#666666')
                  .margin({ top: 8 })
                  .maxLines(2)
                  .textOverflow({ overflow: TextOverflow.Ellipsis })
              }
              .alignItems(HorizontalAlign.Start)
              .layoutWeight(1)

              Text(message.time)
                .fontSize(12)
                .fontColor('#999999')
            }
            .width('100%')
            .padding(16)
            .alignItems(VerticalAlign.Top)
          }
          .backgroundColor('#FFFFFF')
          .margin({ bottom: 1 })
        })
      }
      .layoutWeight(1)
      .backgroundColor('#F5F5F5')
    }
    .width('100%')
    .height('100%')
  }
}

// 购物车页面
@Component
struct CartPage {
  @State cartItems: CartItem[] = [
    { id: 1, name: '老北京炸酱面', price: 28, count: 1, image: $r('app.media.Merchant_Noodle_icon') },
    { id: 2, name: '招牌寿司拼盘', price: 58, count: 2, image: $r('app.media.Merchant_Sushi_icon') }
  ];

  getTotalPrice(): number {
    return this.cartItems.reduce((total, item) => total + item.price * item.count, 0);
  }

  build() {
    Column() {
      // 顶部标题
      Row() {
        Text('购物车')
          .fontSize(18)
          .fontWeight(FontWeight.Medium)
      }
      .width('100%')
      .height(50)
      .justifyContent(FlexAlign.Center)
      .backgroundColor('#FED700')

      if (this.cartItems.length === 0) {
        // 空购物车状态
        Column() {
          Image($r('app.media.Empty_Cart_icon'))
            .width(80)
            .height(80)
            .margin({ bottom: 16 })
          Text('购物车空空如也')
            .fontSize(16)
            .fontColor('#666666')
        }
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else {
        // 购物车商品列表
        Column() {
          List() {
            ForEach(this.cartItems, (item:CartItem) => {
              ListItem() {
                Row() {
                  Image(item.image)
                    .width(60)
                    .height(60)
                    .borderRadius(8)
                    .objectFit(ImageFit.Cover)

                  Column() {
                    Text(item.name)
                      .fontSize(16)
                      .fontWeight(FontWeight.Medium)
                    Text(`￥${item.price}`)
                      .fontSize(14)
                      .fontColor('#FF5722')
                      .margin({ top: 8 })
                  }
                  .alignItems(HorizontalAlign.Start)
                  .layoutWeight(1)
                  .margin({ left: 12 })

                  Row() {
                    Button('-')
                      .width(30)
                      .height(30)
                      .fontSize(16)
                      .backgroundColor('#F5F5F5')
                      .fontColor('#333333')
                      .onClick(() => {
                        if (item.count > 1) {
                          item.count--;
                        }
                      })

                    Text(item.count.toString())
                      .fontSize(16)
                      .margin({ left: 12, right: 12 })

                    Button('+')
                      .width(30)
                      .height(30)
                      .fontSize(16)
                      .backgroundColor('#FED700')
                      .fontColor('#FFFFFF')
                      .onClick(() => {
                        item.count++;
                      })
                  }
                }
                .width('100%')
                .padding(16)
                .alignItems(VerticalAlign.Center)
              }
              .backgroundColor('#FFFFFF')
              .margin({ bottom: 1 })
            })
          }
          .layoutWeight(1)

          // 结算栏
          Row() {
            Text(`总计: ￥${this.getTotalPrice()}`)
              .fontSize(18)
              .fontWeight(FontWeight.Medium)
              .fontColor('#FF5722')
              .layoutWeight(1)

            Button('去结算')
              .width(120)
              .height(40)
              .backgroundColor('#FED700')
              .fontColor('#FFFFFF')
              .onClick(() => {
                // 跳转到结算页面
                router.pushUrl({ url: 'pages/Checkout' });
              })
          }
          .width('100%')
          .padding(16)
          .backgroundColor('#FFFFFF')
          .border({ width: { top: 1 }, color: '#F0F0F0' })
        }
        .layoutWeight(1)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
  }
}

// 我的页面
@Component
struct MinePage {
  build() {
    Column() {
      // 顶部标题
      Row() {
        Text('我的')
          .fontSize(18)
          .fontWeight(FontWeight.Medium)
      }
      .width('100%')
      .height(50)
      .justifyContent(FlexAlign.Center)
      .backgroundColor('#FED700')

      Scroll() {
        Column() {
          // 用户信息卡片
          Row() {
            Image($r('app.media.Avatar_icon'))
              .width(60)
              .height(60)
              .borderRadius(30)

            Column() {
              Text('用户昵称')
                .fontSize(18)
                .fontWeight(FontWeight.Medium)
              Text('手机号: 138****8888')
                .fontSize(14)
                .fontColor('#666666')
                .margin({ top: 4 })
            }
            .alignItems(HorizontalAlign.Start)
            .layoutWeight(1)
            .margin({ left: 16 })

            Image($r('app.media.arrow_back_icon'))
              .width(16)
              .height(16)
          }
          .width('100%')
          .padding(20)
          .backgroundColor('#FFFFFF')
          .borderRadius(12)
          .margin({ top: 16, left: 12, right: 12 })

          // 功能菜单
          Column() {
            this.MenuItemBuilder('我的订单', $r('app.media.History_icon'), 'pages/MyOrders')
            this.MenuItemBuilder('收货地址', $r('app.media.Address_icon'), 'pages/Address')
            this.MenuItemBuilder('优惠券', $r('app.media.Coupon_icon'), 'pages/Coupon')
            this.MenuItemBuilder('客服中心', $r('app.media.Customer_Service_icon'), 'pages/Service')
            this.MenuItemBuilder('设置', $r('app.media.Settings_icon'), 'pages/Settings')
          }
          .backgroundColor('#FFFFFF')
          .borderRadius(12)
          .margin({ top: 16, left: 12, right: 12 })
        }
      }
      .layoutWeight(1)
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
  }

  @Builder
  MenuItemBuilder(title: string, icon: Resource, url: string) {
    Row() {
      Image(icon)
        .width(24)
        .height(24)
        .margin({ right: 12 })

      Text(title)
        .fontSize(16)
        .layoutWeight(1)

      Image($r("app.media.arrow_back_icon"))
        .width(16)
        .height(16)
    }
    .width('100%')
    .height(56)
    .padding({ left: 20, right: 20 })
    .onClick(() => {
      router.pushUrl({ url: url });
    })
    .gesture(
      TapGesture()
        .onAction(() => {
          // 添加点击反馈效果
        })
    )
  }
}