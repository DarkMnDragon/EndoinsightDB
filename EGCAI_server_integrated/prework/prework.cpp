#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define For(i, j, k) for (int i = j; i <= k; i++)
#define DFor(i, j, k) for (int i = j; i >= k; i--)
#define W(a, b) memset(a, b, sizeof(a))
int v_in()
{
    int sum = 0, f = 1;
    char c = getchar();
    while (!isdigit(c)) {
        if (c == '-')
            f = -1;
        c = getchar();
    }
    while (isdigit(c)) {
        sum = (sum << 3) + (sum << 1) + (c ^ 48);
        c = getchar();
    }
    return sum * f;
}
const int M = 2e6 + 5;
string s;
int totq, toto, totql;
struct ques {
    int q;
    int o;
};
stack<int> st0, st2;
stack<ques> st1;
struct question {
    int id, input_type_id, survey_id, level;
    string text;
} q[M];
struct option {
    int id, question_id;
    string opt;
} o[M];
struct question_logic {
    int id, Parent_question_id, Parent_option_id, Child_question_id;
} ql[M];
void solve()
{
    totq = toto = totql = 0;
    while (1) {
        cin >> s;
        if (s == "EOF")
            break;
        int x = 0, level;
        int len = s.length();
        while (x < len && s[x] == '+')
            x++;
        level = x;
        if (s[x] >= '0' && s[x] <= '9') {
            totq++;
            int num = 0, l = x, r = x;
            while (l < len && s[l] != '.')
                num = num * 10 + s[l] - 48, l++;
            /* assert(q[totq].id == num); */
            // 序号从1开始自增
            q[totq].id = totq;
            // 或序号参考survey.txt
            /* q[totq].id = num; */
            q[totq].level = level;
            if (!st1.empty()) {
                while (!st1.empty()) {
                    totql++;
                    ql[totql].id = totql;
                    ql[totql].Parent_question_id = st1.top().q;
                    ql[totql].Parent_option_id = st1.top().o;
                    ql[totql].Child_question_id = totq;
                    st1.pop();
                }
                while (!st2.empty() && q[st2.top()].level > q[totq].level) {
                    totql++;
                    ql[totql].id = totql;
                    ql[totql].Parent_question_id = st2.top();
                    ql[totql].Parent_option_id = 0;
                    ql[totql].Child_question_id = totq;
                    st2.pop();
                }
            } else if (totq > 1) {
                totql++;
                ql[totql].id = totql;
                ql[totql].Parent_question_id = totq - 1;
                ql[totql].Parent_option_id = 0;
                ql[totql].Child_question_id = totq;
                st2.pop();
                if (!st0.empty() && q[totq].level <= q[st0.top()].level) {
                    st0.pop();
                }
            }
            l++;
            r = l;
            while (r < len && s[r] != '?')
                r++;
            q[totq].text = s.substr(l, r - l + 1);
            l = r;
            while (l < len && s[l] != '*' && s[l] != '^' && s[l] != '#')
                l++;
            if (s[l] == '*')
                q[totq].input_type_id = 0, st2.push(totq);
            else if (s[l] == '^')
                q[totq].input_type_id = 1, st0.push(totq);
            else if (s[l] == '#')
                q[totq].input_type_id = 2, st0.push(totq);
            else {
                cout << "错误的输入类型" << endl;
                return;
            }
            q[totq].survey_id = 1;
        } else {
            int pre = st0.top();
            if (level == q[pre].level) {
                toto++;
                o[toto].id = toto;
                o[toto].question_id = pre;
                o[toto].opt = s.substr(x, len - x);
                st1.push((ques) { pre, toto });
            } else if (level < q[pre].level) {
                while (!st0.empty() && level < q[pre].level) {
                    st0.pop();
                    pre = st0.top();
                }
                toto++;
                o[toto].id = toto;
                o[toto].question_id = pre;
                o[toto].opt = s.substr(x, len - x);
                st1.push((ques) { pre, toto });
            }
        }
    }
    cout << "{\n";
    cout << "  \"surveys\": [\n";
    cout << "    {\n";
    cout << "      \"survey_id\": 1,\n";
    cout << "      \"title\": \"疾病预测问卷调查\",\n";
    cout << "      \"description\": \"欢迎参与 EndoInsightDB 问卷调查\\n\\n";
    cout << "尊敬的用户，感谢您参与我们的健康问卷调查。在您开始填写问卷之前，请仔细阅读以下注意事项：\\n\\n";
    cout << "数据隐私和保密性\\n";
    cout << "- 保护您的隐私：我们非常重视您的个人信息和医疗数据的隐私。所有收集的数据将被严格保密，并仅用于医疗研究和改善医疗服务。\\n";
    cout << "- 匿名处理：您的问卷回答将匿名处理，不会泄露您的身份信息。\\n";
    cout << "- 数据安全：我们使用先进的加密技术来保护您的数据安全，防止未经授权的访问。\\n\\n";
    cout << "问卷填写指南\\n";
    cout << "- 仔细阅读每个问题：请在回答每个问题之前仔细阅读题目和选项，确保您完全理解问题的含义。\\n";
    cout << "- 真实准确：请根据您的真实情况回答问题，这对于我们的研究和分析至关重要。\\n";
    cout << "- 完整填写：请尽可能完整地填写问卷，不完整的信息可能会影响问卷的准确性和有效性。\\n";
    cout << "- 随时保存：在填写过程中，您可以随时保存已完成的部分，以防数据丢失。\\n\\n";
    cout << "问卷用途\\n";
    cout << "- 医学研究：您提供的信息将用于消化道疾病的医学研究，帮助医学专家更好地了解疾病模式和趋势。\\n";
    cout << "- 疾病预防和治疗：问卷数据将有助于开发更有效的疾病预防和治疗策略，最终提高患者的生活质量。\\n";
    cout << "- 用户教育：通过分析问卷数据，我们可以更有效地提供健康教育和疾病预防信息。\\n\\n";
    cout << "其他事项\\n";
    cout << "- 自愿参与：您的参与是完全自愿的。如果您在任何时候选择退出问卷，不会有任何不利后果。\\n";
    cout << "- 反馈机制：如果您对问卷有任何疑问或需要帮助，可以通过 1598744255@qq.com 联系我们。\\n\\n";
    cout << "再次感谢您的宝贵时间和参与。您的每一次回答都是对消化道健康研究的宝贵贡献！\",\n";
    cout << "      \"date\": \"2023-11-03\",\n";
    cout << "      \"first_question_id\": 1,\n";
    cout << "      \"last_question_id\": " << totq << "\n";
    cout << "    }\n";
    cout << "  ],\n";
    cout << "  \"input_type\": [\n";
    cout << "    {\n";
    cout << "      \"type_id\": 0,\n";
    cout << "      \"name\": \"填空\"\n";
    cout << "    },\n";
    cout << "    {\n";
    cout << "      \"type_id\": 1,\n";
    cout << "      \"name\": \"单选\"\n";
    cout << "    },\n";
    cout << "    {\n";
    cout << "      \"type_id\": 2,\n";
    cout << "      \"name\": \"多选\"\n";
    cout << "    }\n";
    cout << "  ],\n";
    cout << "  \"questions\": [" << endl;
    For(i, 1, totq)
    {
        cout << "    " << '{' << endl;
        cout << "      \"question_id\": " << q[i].id << ',' << endl;
        cout << "      \"question_text\": \"" << q[i].text << "\"," << endl;
        cout << "      \"type_id\": " << q[i].input_type_id << ',' << endl;
        cout << "      \"survey_id\": " << q[i].survey_id << endl;
        if (i != totq)
            cout << "    }," << endl;
        else
            cout << "    }" << endl;
    }
    cout << "  ]," << endl;
    cout << "  \"options\": [" << endl;
    For(i, 1, toto)
    {
        cout << "    " << '{' << endl;
        cout << "      \"option_id\": " << o[i].id << ',' << endl;
        cout << "      \"option_text\": \"" << o[i].opt << "\"," << endl;
        cout << "      \"question_id\": " << o[i].question_id << endl;
        if (i != toto)
            cout << "    }," << endl;
        else
            cout << "    }" << endl;
    }
    cout << "  ]," << endl;
    cout << "  \"question_logic\": [" << endl;
    For(i, 1, totql)
    {
        cout << "    " << '{' << endl;
        cout << "      \"logic_id\": " << ql[i].id << ',' << endl;
        cout << "      \"parent_question_id\": " << ql[i].Parent_question_id << ',' << endl;
        cout << "      \"parent_option_id\": " << ql[i].Parent_option_id << ',' << endl;
        cout << "      \"child_question_id\": " << ql[i].Child_question_id << endl;
        if (i != totql)
            cout << "    }," << endl;
        else
            cout << "    }" << endl;
    }
    cout << "  ]" << endl
         << "}";
}
int main()
{
    freopen("survey.txt", "r", stdin);
    freopen("survey.json", "w", stdout);
    int T = 1;
    while (T--)
        solve();
    return 0;
}
