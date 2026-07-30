# 和其它 #6 PR

| PR | 做法 | 看法 |
|----|------|------|
| [#54](https://github.com/Tencent/VulnGym/pull/54) | 六条都改了，方向是离开 sanitizer/静态表/非执行点 | 主结论同向 |
| [#77](https://github.com/Tencent/VulnGym/pull/77) | Tournament 构造当 critical；verify=1 | 不采用 |

本 PR 六条：00099/100→evaluateExpression；00103→修 entry+保留 trim 根因；00176→task_analyzer 判断；00511→apply；00512→可写 __sanitize。
