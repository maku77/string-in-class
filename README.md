# string_in_jar.py
Extracts all string literals from Java classes in JAR

JAR ファイル内のクラスファイルから、文字列リテラルだけをすべて抽出するツールです。
内部で `javap` コマンドを使用しているため、Python と JDK がインストールされている必要があります。

## 使い方

```
$ python string_in_jar.py <JARファイル>
```

## 仕組み

1. JAR ファイル内のクラスファイルに対して、ひとつずつ `javap -c` コマンドをかける
2. その出力から `// String xxxx` というテキストを見つけて、`xxxx` の部分だけを出力する
