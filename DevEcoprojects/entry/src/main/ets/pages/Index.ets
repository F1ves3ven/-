import { router } from '@kit.ArkUI'
@Entry
@Component
struct Index {
  pathStack : NavPathStack = new NavPathStack();


  build() {
    Navigation(this.pathStack){
    }.onAppear(() => {
      this.pathStack.pushPathByName("Welcome", null, false);
    })
    .hideNavBar(true)
  }
}
