# 環境構築tips

vuetifyプロジェクトの作成

**下記動作確認済み**

```
npm install vuetify@latest
npm create vuetify@latest
npm run dev
```


**以下、うまく行かず**

```
npm create vite@latest ui -- --template vue
cd ui
npm install
```

```
npm install vuetify@latest
npm install vite-plugin-vuetify --save-dev
npm install sass sass-loader --save-dev
```


## Keycloak設定

realm `local-dev`を作成する。

client `frontend`を作成する。
設定内容は下記の通り。

![img.png](img.png)

![img_1.png](img_1.png)

![img_2.png](img_2.png)


crient secretの生成



## FastAPIの設定



Keycloak Middlewareを使用する。






