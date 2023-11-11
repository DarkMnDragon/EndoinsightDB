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
stack<int> st;
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
            if (!st.empty() && q[totq].level > q[st.top()].level) {
                totql++;
                ql[totql].id = totql;
                ql[totql].Parent_question_id = st.top();
                ql[totql].Parent_option_id = toto;
                ql[totql].Child_question_id = totq;
            } else if (totq > 1) {
                totql++;
                ql[totql].id = totql;
                ql[totql].Parent_question_id = totq - 1;
                ql[totql].Child_question_id = totq;
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
                q[totq].input_type_id = 0;
            else if (s[l] == '^')
                q[totq].input_type_id = 1, st.push(totq);
            else if (s[l] == '#')
                q[totq].input_type_id = 2, st.push(totq);
            else {
                cout << "错误的输入类型" << endl;
                return;
            }
            q[totq].survey_id = 1;
        } else {
            int pre = st.top();
            if (level == q[pre].level) {
                toto++;
                o[toto].id = toto;
                o[toto].question_id = pre;
                o[toto].opt = s.substr(x, len - x);

            } else if (level < q[pre].level) {
                while (!st.empty() && level < q[pre].level) {
                    st.pop();
                    pre = st.top();
                }
                toto++;
                o[toto].id = toto;
                o[toto].question_id = pre;
                int len = s.length();
                o[toto].opt = s.substr(x, len - x);
            }
        }
    }

    cout << "  \"Question\": [" << endl;
    For(i, 1, totq)
    {
        cout << "    " << '{' << endl;
        cout << "      \"Question_id\": " << q[i].id << ',' << endl;
        cout << "      \"Text\": \"" << q[i].text << "\"," << endl;
        cout << "      \"Input_type_id\": " << q[i].input_type_id << ',' << endl;
        cout << "      \"Survey_id\": " << q[i].survey_id << endl;
        cout << "    }," << endl;
    }
    cout << "  ]," << endl;
    cout << "  \"Options\": [" << endl;
    For(i, 1, toto)
    {
        cout << "    " << '{' << endl;
        cout << "      \"Option_id\": " << o[i].id << ',' << endl;
        cout << "      \"option_text\": \"" << o[i].opt << "\"," << endl;
        cout << "      \"Question_id\": " << o[i].question_id << endl;
        cout << "    }," << endl;
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
        cout << "    }," << endl;
    }
    cout << "  ]" << endl;
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
