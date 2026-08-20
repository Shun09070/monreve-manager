monrêve Manager v12 Gemini内蔵準備版
1. GitHub Pagesは index.html を差し替えます。
2. backend をGoogle Cloud Runへデプロイします。
3. GEMINI_API_KEYはCloud Run側の環境変数/Secret Managerに設定し、GitHubには書きません。
4. Cloud Run URL + /analyze をアプリのGemini接続先に登録します。
5. 「Geminiに相談する」でアプリ内に回答が表示されます。
