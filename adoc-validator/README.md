# adoc-validator

AsciiDocで記述された仕様書が[記述ルール](https://github.tmc-stargate.com/bevdev-body/swe-template/blob/main/doc/README.md#asciidocドキュメントの文書記載ルール)に従っているかを検査します。

## Usage

``` yaml
- uses: bevdev-body/swe-actions/adoc-validator@stable
  with:
    input_dir: {path/to/adocs} #検査する*.adocファイルが配置されたディレクトリ
```

- `input_dir`: 実行中のワークフローの作業ディレクトリからの相対パス、または、GitHub Actionsにおける[環境変数](https://docs.github.com/ja/actions/learn-github-actions/variables#default-environment-variables)や[コンテキスト](https://docs.github.com/ja/actions/learn-github-actions/contexts)を使用した絶対パスで対象のディレクトリを指定します。指定されたディレクトリを再帰的に検索し、検出されたすべての `*.adoc` ファイルを検査します。

## Supported Platforms

本アクションはWindows(x64)上で動作するセルフホステッドランナーでのみ動作を確認しています。
