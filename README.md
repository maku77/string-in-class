# string_in_class.py
Extracts all string literals from Java classes

指定した Java クラスファイルや、JAR ファイル内のクラスファイルから、文字列リテラルだけをすべて抽出するツールです。
内部で `javap` コマンドを使用しているため、Python と JDK がインストールされている必要があります。

## 使い方

```
$ python string_in_class.py <JARファイル or CLASSファイル>
```

## 仕組み

1. JAR ファイル内のクラスファイルに対して、ひとつずつ `javap -c` コマンドをかける
2. その出力から `#12 = String   #34  // xxxx` といったテキストを見つけて、`xxxx` の部分だけを出力する

