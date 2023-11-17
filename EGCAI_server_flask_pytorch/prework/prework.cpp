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
            q[totq].id = totq;
            int num = 0, l = x, r = x;
            while (l < len && s[l] != '.')
                num = num * 10 + s[l] - 48, l++;
            assert(q[totq].id == num);
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
                q[totq].input_type_id = 2, st2.push(totq);
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
    cout << "{\n  \"Surveys\": [\n    {\n      \"Survey_id\": 1,\n      \"Title\": \"问卷调查\",\n      \"Description\": \"\",\n      \"Date\": \"2023-11-03\",\n      \"first_question_id\": 1,\n      \"last_question_id\": 66\n    }\n  ],\n";
    cout << "  \"Input_type\": [\n    {\n      \"Input_type_id\": 0,\n      \"Name\": \"填空\"\n    },\n    {\n      \"Input_type_id\": 1,\n      \"Name\": \"单选\"\n    },\n    {\n      \"Input_type_id\": 2,\n      \"Name\": \"多选\"\n    }\n  ],\n";
    cout << "  \"Questions\": [" << endl;
    For(i, 1, totq)
    {
        cout << "    " << '{' << endl;
        cout << "      \"Question_id\": " << q[i].id << ',' << endl;
        cout << "      \"Text\": \"" << q[i].text << "\"," << endl;
        cout << "      \"Input_type_id\": " << q[i].input_type_id << ',' << endl;
        cout << "      \"Survey_id\": " << q[i].survey_id << endl;
        if (i != totq)
            cout << "    }," << endl;
        else
            cout << "    }" << endl;
    }
    cout << "  ]," << endl;
    cout << "  \"Options\": [" << endl;
    For(i, 1, toto)
    {
        cout << "    " << '{' << endl;
        cout << "      \"Option_id\": " << o[i].id << ',' << endl;
        cout << "      \"option_text\": \"" << o[i].opt << "\"," << endl;
        cout << "      \"Question_id\": " << o[i].question_id << endl;
        if (i != toto)
            cout << "    }," << endl;
        else
            cout << "    }" << endl;
    }
    cout << "  ]," << endl;
    cout << "  \"Question_logic\": [" << endl;
    For(i, 1, totql)
    {
        cout << "    " << '{' << endl;
        cout << "      \"Logic_id\": " << ql[i].id << ',' << endl;
        cout << "      \"Parent_question_id\": " << ql[i].Parent_question_id << ',' << endl;
        cout << "      \"Parent_option_id\": " << ql[i].Parent_option_id << ',' << endl;
        cout << "      \"Child_question_id\": " << ql[i].Child_question_id << endl;
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
