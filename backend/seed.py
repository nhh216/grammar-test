"""Seed script: insert predefined TOEIC grammar topics with detailed summaries."""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.grammar_topic import GrammarTopic

TOPICS = [
    {
        "name": "Tenses",
        "slug": "tenses",
        "description": "Present, past, future, perfect, and continuous tenses used in TOEIC contexts",
        "summary": """## Các Thì Động Từ (Tenses)

---

## Bản Đồ 12 Thì

| | Simple | Continuous | Perfect | Perfect Continuous |
|--|--------|------------|---------|-------------------|
| **Present** | V/V-s | am/is/are V-ing | have/has V3 | have/has been V-ing |
| **Past** | V2/ed | was/were V-ing | had V3 | had been V-ing |
| **Future** | will V | will be V-ing | will have V3 | will have been V-ing |

---

## 1. Thì Hiện Tại Đơn (Simple Present)

**Cấu trúc:** `S + V(s/es)`

**Khi nào dùng:**
- Thói quen, hành động lặp lại thường xuyên
- Sự thật hiển nhiên, quy luật khoa học
- Lịch trình cố định (thời khóa biểu, tàu xe)
- Mệnh đề điều kiện & thời gian thay cho tương lai

**Dấu hiệu nhận biết:** always, usually, often, sometimes, rarely, never, every day/week/month, on Mondays

:::example
- She **checks** her email every morning.
- The store **opens** at 9 AM on weekdays.
- Water **boils** at 100°C.
- If he **arrives**, call me. *(KHÔNG dùng "will arrive")*
- When she **finishes**, we will leave. *(KHÔNG dùng "will finish")*
:::

:::warning
Mệnh đề **if/when/before/after/as soon as/once/until** → KHÔNG dùng will, dùng Present Simple thay thế.
:::

---

## 2. Thì Hiện Tại Tiếp Diễn (Present Continuous)

**Cấu trúc:** `S + am/is/are + V-ing`

**Khi nào dùng:**
- Hành động đang xảy ra ngay lúc nói
- Xu hướng tạm thời trong thời gian gần
- Kế hoạch đã sắp xếp trong tương lai gần

**Dấu hiệu nhận biết:** now, at the moment, currently, right now, this week/month, still

:::example
- The team **is reviewing** the proposal right now.
- Sales **are increasing** steadily this quarter.
- She **is meeting** the client tomorrow afternoon. *(kế hoạch đã sắp xếp)*
:::

:::warning
**Stative verbs** KHÔNG dùng continuous: know, believe, understand, want, need, like, love, hate, seem, appear, contain, belong, own, exist
- ❌ I am knowing the answer. → ✅ I know the answer.
- ❌ She is having a car. → ✅ She has a car. (sở hữu)
- ✅ She is having lunch. (hành động → OK)
:::

---

## 3. Thì Hiện Tại Hoàn Thành (Present Perfect)

**Cấu trúc:** `S + have/has + V3 (past participle)`

**Khi nào dùng:**
- Hành động xảy ra trong quá khứ, kết quả còn ảnh hưởng đến hiện tại
- Kinh nghiệm tích lũy (đã từng làm gì)
- Hành động vừa mới xảy ra
- Hành động bắt đầu từ quá khứ, kéo dài đến hiện tại

**Dấu hiệu nhận biết:** already, yet, just, ever, never, recently, lately, since + mốc thời gian, for + khoảng thời gian, so far, up to now, this week/month/year

:::example
- The company **has launched** three new products this year.
- She **has worked** here since 2019. *(vẫn đang làm)*
- We **have just received** your application.
- **Have** you ever **attended** an international conference?
:::

:::warning
**Present Perfect vs Past Simple:**
- ❌ I have visited Paris **last year**. → ✅ I **visited** Paris last year. (last year → past simple)
- ❌ She **worked** here **since** 2020. → ✅ She **has worked** here since 2020. (since → present perfect)
:::

:::tip
**Since vs For:** "since 2020" = từ mốc thời gian cụ thể | "for 3 years" = khoảng thời gian kéo dài
:::

---

## 4. Thì Hiện Tại Hoàn Thành Tiếp Diễn (Present Perfect Continuous)

**Cấu trúc:** `S + have/has been + V-ing`

**Khi nào dùng:** Hành động bắt đầu quá khứ, vẫn đang tiếp diễn, nhấn mạnh **thời gian**.

:::example
- She **has been working** here for 5 years. *(vẫn đang làm)*
- I **have been waiting** for 2 hours.
- They **have been negotiating** since Monday.
:::

:::tip
**Phân biệt:**
- I **have read** the book → đã đọc xong
- I **have been reading** the book → vẫn đang đọc
:::

---

## 5. Thì Quá Khứ Đơn (Simple Past)

**Cấu trúc:** `S + V2/V-ed`

**Khi nào dùng:** Hành động hoàn thành tại thời điểm xác định trong quá khứ.

**Dấu hiệu nhận biết:** yesterday, last week/month/year, ago, in 2020, when + quá khứ

:::example
- The board **approved** the merger last Tuesday.
- She **joined** the company in 2018 and **became** manager in 2021.
- When the system **crashed**, the team **immediately contacted** IT support.
:::

---

## 6. Thì Quá Khứ Tiếp Diễn (Past Continuous)

**Cấu trúc:** `S + was/were + V-ing`

**Khi nào dùng:**
- Đang xảy ra tại một thời điểm trong quá khứ
- Hành động bị gián đoạn (when + past simple)
- Hai hành động song song (while)

:::example
- I **was working** at 9 PM last night.
- She **was reading** when he called. *(was reading bị gián đoạn)*
- While he **was cooking**, she **was cleaning**.
:::

---

## 7. Thì Quá Khứ Hoàn Thành (Past Perfect)

**Cấu trúc:** `S + had + V3`

**Khi nào dùng:** Hành động xảy ra **trước** một hành động khác trong quá khứ.

**Dấu hiệu nhận biết:** before, after, when, by the time, already, just, never...before

:::example
- When he **arrived**, she **had already left**.
- They **had finished** the project before the deadline.
- By the time the manager arrived, the team **had completed** the report.
:::

---

## 8. Thì Quá Khứ Hoàn Thành Tiếp Diễn (Past Perfect Continuous)

**Cấu trúc:** `S + had been + V-ing`

**Khi nào dùng:** Nhấn mạnh thời gian hành động kéo dài trước một thời điểm trong quá khứ.

:::example
- She **had been working** for 3 hours when he called.
- They **had been negotiating** for weeks before reaching an agreement.
:::

---

## 9. Thì Tương Lai (Future)

| Cấu trúc | Dùng khi | Ví dụ |
|-----------|----------|-------|
| `will + V` | Quyết định tức thì, dự đoán, lời hứa | I **will help** you. |
| `be going to + V` | Kế hoạch đã định, dự đoán có bằng chứng | We **are going to expand**. |
| `will be + V-ing` | Đang xảy ra tại thời điểm tương lai | I **will be flying** to Tokyo. |
| `will have + V3` | Hoàn thành trước thời điểm tương lai | She **will have finished** by Friday. |
| `Simple Present` | Lịch trình cố định | The flight **departs** at 6 AM. |

:::example
- I **will help** you with that report. *(quyết định tức thì)*
- Look at those clouds — it **is going to rain**. *(dự đoán có bằng chứng)*
- By Friday, she **will have finished** the report.
- This time tomorrow, I **will be flying** to Tokyo.
:::

---

## Bảng Signal Words Tổng Hợp

| Thì | Từ nhận biết |
|-----|-------------|
| Present Simple | always, usually, often, every day/week |
| Present Continuous | now, at the moment, currently, at present |
| Present Perfect | just, already, yet, ever, never, since, for, recently, so far |
| Past Simple | yesterday, ago, last..., in + năm, when |
| Past Perfect | before, after, by the time, already, never...before |
| Future Simple | tomorrow, next week, soon |
| Future Perfect | by + future time |

---

:::tip
**Mẹo làm bài TOEIC:**
- **By + time future** → will have + V3 | **By + time past** → had + V3 | **By now** → have/has + V3
- **Since/for** → Present Perfect hoặc Perfect Continuous
- Mệnh đề **if/when/before/after/as soon as/once/until** → Present Simple (không dùng will)
- **No sooner had...than / Hardly had...when** → Đảo ngữ + Past Perfect
- **used to + V** = thói quen quá khứ (không còn nữa); **would + V** = hành động lặp lại quá khứ (không dùng cho trạng thái)
:::
""",
    },
    {
        "name": "Articles",
        "slug": "articles",
        "description": "Correct usage of a, an, and the in English sentences",
        "summary": """## Mạo Từ (Articles)

---

## 1. Mạo Từ Không Xác Định: A / AN

**Quy tắc chọn A hay AN — dựa vào ÂM THANH, không phải chữ cái:**

| | Ví dụ |
|--|-------|
| **A** → trước âm phụ âm | a book, a car, a **u**niversity (/j/), a **eu**ropean (/j/), a **o**ne-way street (/w/) |
| **AN** → trước âm nguyên âm | an apple, an **h**our (h câm), an **M**BA (/em/), an **X**-ray (/eks/) |

**Khi nào dùng A/AN:**

| Trường hợp | Ví dụ |
|-----------|-------|
| Đề cập lần đầu, chưa xác định | I saw **a** man in the lobby. |
| Nghề nghiệp, danh hiệu | She is **an** engineer. He was elected **a** director. |
| Mang nghĩa "một" | Please give me **a** moment. |
| Trong cụm cố định | **such a**, **what a**, **quite a**, **rather a**, **half a** |
| Mỗi (per) | twice **a** week, $50 **a** day, 80 km **an** hour |

---

## 2. Mạo Từ Xác Định: THE

**Khi nào dùng THE:**

| Trường hợp | Ví dụ |
|-----------|-------|
| Đã đề cập lần trước | I saw a man. **The** man was carrying a briefcase. |
| Cả hai bên đã biết | Please close **the** door. Sign **the** contract. |
| Danh từ duy nhất | **the** sun, **the** moon, **the** earth, **the** sky, **the** Internet |
| So sánh nhất | She is **the** best candidate. |
| Số thứ tự | **the** first, **the** second, **the** last |
| Sông, biển, đại dương, dãy núi, quần đảo | **the** Mekong, **the** Pacific, **the** Alps, **the** Philippines |
| Quốc gia có "States/Kingdom/Republic" | **the** United States, **the** United Kingdom |
| Danh từ chỉ cả loài | **The** whale is endangered. |
| Nhạc cụ | She plays **the** piano. |
| Tính từ dùng như danh từ (chỉ nhóm người) | **the** rich, **the** poor, **the** elderly, **the** unemployed |
| Thập kỷ | in **the** 1990s, **the** 20th century |
| Phương tiện truyền thông | **the** radio, **the** newspaper (nhưng: watch **television**) |

---

## 3. Không Dùng Mạo Từ (Zero Article)

| Trường hợp | Ví dụ |
|-----------|-------|
| Danh từ số nhiều nghĩa chung | **Employees** need to complete the form. |
| Danh từ không đếm được nghĩa chung | **Information** is power. **Patience** is a virtue. |
| Tên người, công ty, thành phố, quốc gia (đơn) | **Vietnam**, **Microsoft**, **John**, **Hanoi** |
| Bữa ăn | have **breakfast**, after **lunch**, at **dinner** |
| Phương tiện (by) | by **car**, by **train**, by **air**, by **sea** |
| Môn thể thao, hoạt động | play **football**, do **yoga**, go **swimming** |
| Môn học, ngôn ngữ | study **economics**, speak **English** |
| Bệnh thông thường | have **flu**, have **cancer** (nhưng: have **a cold**, have **a headache**) |
| Tên đường phố, công viên (đơn) | on **Main Street**, in **Central Park** |

:::warning
**Ngoại lệ quan trọng:**
- **the** Internet, **the** news, **the** environment, **the** government, **the** media
- in **the** morning/afternoon/evening (nhưng: at **night**, at **noon**, at **midnight**)
- **the** radio (nghe radio) nhưng watch **television** (không có the)
:::

---

## 4. Phân Biệt Nghĩa: Institution vs Building

| Cụm | Nghĩa |
|-----|-------|
| go to **school** | đi học (học sinh) |
| go to **the school** | đến tòa nhà trường học |
| go to **hospital** *(BrE)* | nhập viện điều trị |
| go to **the hospital** | đến bệnh viện (thăm ai đó) |
| in **prison** | đang bị giam |
| in **the prison** | ở trong tòa nhà nhà tù |
| at **sea** | đang ra khơi |
| at **the sea** | ở gần bãi biển |

---

## 5. Articles Với Tên Riêng

| Loại | Dùng THE | Không dùng |
|------|---------|------------|
| Sông, kênh, biển | the Nile, the Suez Canal, the Black Sea | — |
| Dãy núi | the Alps, the Himalayas | — |
| Quần đảo | the Philippines, the Maldives | — |
| Quốc gia (đơn) | — | Vietnam, France, Japan |
| Quốc gia có "Republic/Kingdom/States" | the USA, the UK, the UAE | — |
| Thành phố, bang | — | Hanoi, California |
| Sân bay, nhà ga | — | Heathrow Airport, Central Station |
| Khách sạn, nhà hàng | the Hilton, the Ritz | — |
| Tạp chí, báo | the New York Times, the Economist | — |

---

:::tip
**Mẹo làm bài TOEIC:**
- Danh từ có **my/his/their/this/that** → KHÔNG dùng mạo từ
- Tên riêng viết hoa → thường không có mạo từ (trừ ngoại lệ)
- Blank trước danh từ số nhiều → zero article hoặc "the" (không phải a/an)
- **The + adj** = danh từ chỉ nhóm người (the rich = những người giàu)
- **Twice/once/three times a + N thời gian** → mang nghĩa "mỗi"
:::
""",
    },
    {
        "name": "Prepositions",
        "slug": "prepositions",
        "description": "Prepositions of time, place, direction, and idiomatic usage",
        "summary": """## Giới Từ (Prepositions)

---

## 1. Giới Từ Thời Gian

| Giới từ | Quy tắc | Ví dụ |
|---------|---------|-------|
| **at** | giờ cụ thể, thời điểm chính xác | at 9 AM, at noon, at midnight, at the weekend |
| **on** | ngày trong tuần, ngày tháng cụ thể, ngày lễ | on Monday, on July 4th, on New Year's Day |
| **in** | tháng, năm, thập kỷ, buổi trong ngày | in March, in 2024, in the morning, in the 21st century |
| **for** | khoảng thời gian kéo dài | for two hours, for a week, for years |
| **since** | mốc thời gian cụ thể (với thì hoàn thành) | since Monday, since 2018, since last year |
| **by** | trước thời điểm (deadline) | by Friday, by 5 PM, by the end of the month |
| **until/till** | cho đến tận khi (tiếp diễn) | until midnight, until further notice |
| **during** | trong suốt khoảng thời gian | during the meeting, during lunch break |
| **within** | trong vòng (không quá) | within 24 hours, within a week |
| **from...to/until** | từ...đến | from Monday to Friday, from 9 to 5 |
| **in** (tương lai) | sau khoảng thời gian | in 3 days, in two weeks |
| **ago** | cách đây | two days ago, a year ago |

:::tip
**within vs in:** within 3 days = không quá 3 ngày | in 3 days = 3 ngày kể từ bây giờ
**by vs until:** by Friday = xong trước thứ Sáu | until Friday = tiếp tục đến thứ Sáu
:::

---

## 2. Giới Từ Nơi Chốn

| Giới từ | Dùng với | Ví dụ |
|---------|---------|-------|
| **at** | điểm/địa điểm cụ thể | at the office, at reception, at the airport |
| **in** | không gian bên trong, khu vực rộng | in the meeting room, in Hanoi, in Vietnam |
| **on** | bề mặt, tầng lầu, phương tiện lớn | on the desk, on the 3rd floor, on the bus/plane |
| **above/below** | phía trên/dưới (không tiếp xúc) | above average, below expectations |
| **over/under** | phía trên/dưới (che phủ/tiếp xúc) | over the bridge, under the table |
| **between** | giữa hai vật/người | between the two buildings |
| **among** | giữa nhiều vật/người | among the employees |
| **next to/beside** | bên cạnh | next to the elevator |
| **opposite** | đối diện | opposite the main entrance |
| **in front of** | phía trước | in front of the building |
| **behind** | phía sau | behind the counter |
| **near/close to** | gần | near the station |

---

## 3. Giới Từ Hướng Đi

| Giới từ | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| **to** | di chuyển đến | go to the office, fly to Tokyo |
| **into** | đi vào bên trong | walk into the room, log into the system |
| **out of** | ra khỏi | get out of the car, step out of the meeting |
| **from** | xuất phát từ | come from Hanoi, a call from the client |
| **through** | xuyên qua | pass through customs, go through the process |
| **across** | băng ngang qua | walk across the street, across the country |
| **along** | dọc theo | walk along the corridor |
| **toward(s)** | hướng về phía | move toward the exit |
| **past** | đi ngang qua | walk past the reception |

---

## 4. Động Từ + Giới Từ (Verb Collocations)

| Cụm | Nghĩa |
|-----|-------|
| apply **for** (position) / apply **to** (organization) | ứng tuyển / nộp đơn đến |
| deal **with** | giải quyết |
| depend **on** | phụ thuộc vào |
| result **in** (hậu quả) / result **from** (nguyên nhân) | dẫn đến / xuất phát từ |
| consist **of** | bao gồm |
| contribute **to** | đóng góp vào |
| comply **with** | tuân thủ |
| specialize **in** | chuyên về |
| inform sb **of/about** | thông báo |
| congratulate sb **on** | chúc mừng về |
| agree **with** (person) / agree **to** (plan) / agree **on** (decision) | đồng ý với |
| focus **on** | tập trung vào |
| insist **on** | khăng khăng |
| succeed **in** | thành công trong |
| refer **to** | đề cập đến |
| respond **to** | phản hồi |
| participate **in** | tham gia |
| invest **in** | đầu tư vào |
| benefit **from** | hưởng lợi từ |
| differ **from** | khác với |
| interfere **with** | can thiệp vào |

---

## 5. Tính Từ + Giới Từ (Adjective Collocations)

| Cụm | Nghĩa |
|-----|-------|
| responsible **for** | chịu trách nhiệm về |
| interested **in** | quan tâm đến |
| familiar **with** | quen thuộc với |
| eligible **for** | đủ điều kiện |
| capable **of** | có khả năng |
| aware **of** | nhận thức được |
| satisfied **with** | hài lòng với |
| committed **to** | cam kết với |
| based **on** | dựa trên |
| related **to** | liên quan đến |
| suitable **for** | phù hợp với |
| dedicated **to** | tận tụy với |
| concerned **about** | lo lắng về |
| proud **of** | tự hào về |
| grateful **for** | biết ơn về |
| disappointed **with/in** | thất vọng về |
| associated **with** | liên quan đến |
| entitled **to** | có quyền nhận |
| accustomed **to** | quen với |

---

## 6. Danh Từ + Giới Từ (Noun Collocations)

| Cụm | Nghĩa |
|-----|-------|
| increase/decrease **in** | tăng/giảm về |
| demand **for** | nhu cầu về |
| reason **for** | lý do cho |
| impact **on** | tác động đến |
| solution **to** | giải pháp cho |
| access **to** | quyền truy cập |
| experience **in** | kinh nghiệm trong |
| advantage **of/over** | lợi thế của/so với |
| relationship **with/between** | mối quan hệ |
| knowledge **of** | kiến thức về |

---

## 7. Cụm Giới Từ Ghép (Prepositional Phrases)

| Cụm | Nghĩa |
|-----|-------|
| **on behalf of** | thay mặt cho |
| **in terms of** | về mặt |
| **with regard to / regarding** | liên quan đến |
| **in addition to** | ngoài ra, bên cạnh |
| **as a result of** | do kết quả của |
| **in accordance with** | theo đúng |
| **in charge of** | phụ trách |
| **in favor of** | ủng hộ |
| **in response to** | để phản hồi |
| **at the expense of** | với chi phí của |
| **in place of** | thay thế cho |
| **prior to** | trước khi |
| **due to / owing to** | do, vì |
| **except for** | ngoại trừ |

---

:::tip
**Mẹo làm bài TOEIC:**
- Học giới từ theo **cụm cố định** (collocation), không học riêng lẻ
- **at/in/on** + thời gian: nhỏ→lớn = at (giờ) → on (ngày) → in (tháng/năm)
- **result in** (hậu quả) ≠ **result from** (nguyên nhân)
- **agree with** (người) / **agree to** (kế hoạch) / **agree on** (quyết định)
- **on behalf of** và **in terms of** thường xuất hiện trong Part 5/6
:::
""",
    },
    {
        "name": "Modal Verbs",
        "slug": "modal-verbs",
        "description": "Can, could, should, must, may, might, would, and will in context",
        "summary": """## Động Từ Khiếm Khuyết (Modal Verbs)

---

## Đặc Điểm Chung

- Không thêm **-s/-es** dù chủ ngữ là he/she/it
- Sau modal → **V nguyên mẫu** (không to)
- Không dùng hai modal liên tiếp
- Phủ định: modal + **not** (can't, couldn't, shouldn't, mustn't, won't...)

---

## 1. Khả Năng và Sự Cho Phép

| Modal | Ý nghĩa | Ví dụ |
|-------|---------|-------|
| **can** | khả năng hiện tại | She **can** speak three languages. |
| **could** | khả năng quá khứ / lịch sự | He **could** solve complex problems. |
| **can / may** | cho phép | You **can/may** use the conference room. |
| **may** | cho phép (trang trọng hơn) | Employees **may** work from home. |
| **be able to** | thay thế can (tất cả thì) | She **was able to** finish on time. |

:::tip
**can** = khả năng/cho phép thông thường | **may** = trang trọng hơn, thường trong văn bản
**be able to** dùng khi cần chia thì: will be able to, have been able to, was able to
:::

---

## 2. Nghĩa Vụ và Sự Cần Thiết

| Modal | Ý nghĩa | Ví dụ |
|-------|---------|-------|
| **must** | bắt buộc (từ người nói / nội quy) | All staff **must** wear ID badges. |
| **have to** | bắt buộc (từ quy định bên ngoài) | She **has to** submit the report by 5 PM. |
| **need to** | cần thiết | We **need to** update the system. |
| **should** | lời khuyên, bổn phận | You **should** proofread before sending. |
| **ought to** | lời khuyên (trang trọng) | Management **ought to** address this issue. |
| **had better** | lời khuyên mạnh (ngầm cảnh báo hậu quả) | You **had better** respond quickly. |

:::warning
| Cụm | Nghĩa |
|-----|-------|
| **must not** | bị cấm tuyệt đối |
| **don't have to / need not** | không cần (không bắt buộc) |
| **had better not** | tốt hơn là đừng |

- You **must not** share your password. *(cấm)*
- You **don't have to** work overtime. *(tự nguyện)*
- You **had better not** miss the deadline. *(cảnh báo)*
:::

---

## 3. Dự Đoán và Suy Luận (Theo Mức Độ Chắc Chắn)

| Modal | Mức độ | Ví dụ |
|-------|--------|-------|
| **will** | chắc chắn ~100% | The meeting **will** start at 9. |
| **must** | suy luận chắc ~95% | She's not here — she **must** be in a meeting. |
| **should/ought to** | gần chắc ~90% | The package **should** arrive tomorrow. |
| **may** | có thể ~50% | The project **may** be delayed. |
| **might/could** | ít khả năng ~30% | It **might** rain this afternoon. |
| **can't/couldn't** | không thể (phủ nhận logic) | He **can't** be in the office — I just saw him leave. |

---

## 4. Yêu Cầu và Đề Nghị Lịch Sự

| Cấu trúc | Mức độ lịch sự |
|----------|--------------|
| Can you...? | thông thường |
| Could you...? | lịch sự hơn |
| Would you...? | lịch sự, trang trọng |
| Would you mind + V-ing...? | rất lịch sự |
| May I...? | xin phép lịch sự |
| Shall I...? | đề nghị giúp đỡ |

---

## 5. Modal + Have + V3 (Nói Về Quá Khứ)

| Cấu trúc | Ý nghĩa | Ví dụ |
|----------|---------|-------|
| **should have + V3** | lẽ ra phải làm (nhưng không làm) | You **should have submitted** the form earlier. |
| **shouldn't have + V3** | lẽ ra không nên làm (nhưng đã làm) | We **shouldn't have ignored** the warning. |
| **could have + V3** | lẽ ra có thể làm (nhưng không làm) | We **could have avoided** this problem. |
| **must have + V3** | chắc hẳn đã làm (suy luận quá khứ) | She **must have forgotten** the meeting. |
| **might/may have + V3** | có thể đã làm (không chắc) | He **might have missed** the announcement. |
| **can't have + V3** | không thể nào đã làm | They **can't have left** already. |
| **would have + V3** | lẽ ra đã làm (điều kiện loại 3) | We **would have won** if we had prepared better. |

---

## 6. Would: Các Nghĩa Khác

| Nghĩa | Ví dụ |
|-------|-------|
| Thói quen trong quá khứ | He **would** visit the office every Monday. |
| Sở thích lịch sự | I **would** prefer the afternoon session. |
| Lời mời/đề nghị | **Would** you like some coffee? |
| Điều kiện | If I had time, I **would** attend. |

---

## 7. Dare và Need (Semi-modals)

```
dare / need + V bare (câu phủ định/nghi vấn)
dare to / need to + V (câu khẳng định thông thường)
```

:::example
- **Need** I submit a separate form? *(modal — nghi vấn)*
- I **need to** submit the form. *(normal verb — khẳng định)*
- She **dare not** mention it in front of the CEO.
:::

---

:::tip
**Mẹo làm bài TOEIC:**
- Blank sau modal → V nguyên mẫu (không -ing, không -ed, không to)
- **must not** (cấm) ≠ **don't have to** (không cần)
- **should have + V3** → thường xuất hiện trong Part 6/7 (hối tiếc/phê bình)
- **would** + V = thói quen quá khứ (không dùng cho trạng thái — dùng **used to** thay)
- **be able to** dùng khi cần chia thì đặc biệt (will, have, was/were)
:::
""",
    },
    {
        "name": "Conditionals",
        "slug": "conditionals",
        "description": "Type 0, 1, 2, and 3 conditional sentences",
        "summary": """## Câu Điều Kiện (Conditionals)

---

## Tổng Quan Các Loại Câu Điều Kiện

| Loại | Mệnh đề IF | Mệnh đề chính | Dùng khi |
|------|-----------|--------------|---------|
| **Type 0** | V hiện tại đơn | V hiện tại đơn | Sự thật luôn đúng |
| **Type 1** | V hiện tại đơn | will/can/may + V | Có thể xảy ra ở tương lai |
| **Type 2** | V quá khứ đơn | would/could/might + V | Giả định, trái hiện tại |
| **Type 3** | had + V3 | would/could/might + have + V3 | Trái với thực tế quá khứ |
| **Mixed** | had + V3 | would + V (hiện tại) | QK → ảnh hưởng HT |

---

## 1. Câu Điều Kiện Loại 0 – Sự Thật Hiển Nhiên

**Cấu trúc:** `If/When + S + V (hiện tại đơn), S + V (hiện tại đơn)`

:::example
- If you heat metal, it **expands**.
- If sales **decline**, management **reviews** the strategy.
- If the system **detects** an error, it **sends** an alert automatically.
:::

---

## 2. Câu Điều Kiện Loại 1 – Có Thể Xảy Ra

**Cấu trúc:** `If + S + V (hiện tại đơn), S + will/can/may/should + V`

:::example
- If we **meet** the quarterly target, the team **will receive** a bonus.
- If you **submit** the application today, you **may be** considered.
- If the client **approves** the proposal, we **can** start next week.
:::

---

## 3. Câu Điều Kiện Loại 2 – Giả Định Trái Hiện Tại

**Cấu trúc:** `If + S + V-past, S + would/could/might + V`

:::example
- If I **were** the CEO, I **would implement** a flexible work policy.
- If we **had** a larger budget, we **could expand** to new markets.
:::

:::warning
I/he/she/it → dùng **were** (không phải was) trong văn viết trang trọng:
"If I **were** you, I would reconsider." *(chuẩn TOEIC)*
:::

---

## 4. Câu Điều Kiện Loại 3 – Trái Với Thực Tế Quá Khứ

**Cấu trúc:** `If + S + had + V3, S + would/could/might + have + V3`

:::example
- If they **had submitted** the bid on time, they **would have won** the contract.
- If the manager **had noticed** the error earlier, we **could have corrected** it.
- If she **had taken** the job offer, she **might have** become director by now.
:::

---

## 5. Câu Điều Kiện Hỗn Hợp (Mixed Conditionals)

### Loại A: Điều kiện QK → kết quả HT
`If + had + V3, S + would + V (hiện tại)`

:::example
- If I **had studied** engineering, I **would be** working in a different field now.
- If the company **had invested** in training, our team **would be** more productive today.
:::

### Loại B: Điều kiện HT → kết quả QK
`If + V-past, S + would + have + V3`

:::example
- If she **were** more experienced, she **would have been** selected last year.
:::

---

## 6. Đảo Ngữ Câu Điều Kiện (Inverted Conditionals — Trang Trọng)

Bỏ "if", đảo trợ động từ lên trước chủ ngữ. Thường gặp trong văn bản kinh doanh.

| Loại | Dạng đảo ngữ | Ví dụ |
|------|-------------|-------|
| Type 1 | **Should** + S + V... | **Should** you need assistance, please contact us. |
| Type 2 | **Were** + S + to + V... | **Were** the project to fail, we would revise the plan. |
| Type 3 | **Had** + S + V3... | **Had** we known earlier, we would have acted. |

:::example
- **Should** you have any questions, do not hesitate to contact us.
  = If you have any questions...
- **Had** the team been better prepared, they would have succeeded.
  = If the team had been better prepared...
:::

---

## 7. Mệnh Đề Wish (Ước muốn)

| Wish + | Ý nghĩa | Ví dụ |
|--------|---------|-------|
| **past simple** | ước hiện tại (trái thực) | I wish I **knew** the answer. |
| **past perfect** | ước quá khứ (đã xảy ra rồi) | I wish I **had attended** that meeting. |
| **would + V** | ước tương lai / phàn nàn | I wish he **would respond** faster. |

:::example
- I wish the office **were** larger. *(hiện tại — trái thực)*
- She wishes she **had applied** for the position. *(quá khứ — hối tiếc)*
- I wish the system **would work** properly. *(phàn nàn)*
:::

---

## 8. Các Từ Thay Thế "If"

| Từ/Cụm | Ý nghĩa | Ví dụ |
|--------|---------|-------|
| **unless** | nếu không, trừ phi | **Unless** you confirm, we'll cancel. |
| **provided (that)** | với điều kiện là | You can work from home **provided that** you meet deadlines. |
| **as long as / so long as** | miễn là | The policy applies **as long as** staff follow guidelines. |
| **in case** | phòng khi | Save frequently **in case** the system crashes. |
| **even if** | ngay cả khi | **Even if** it rains, the event will proceed. |
| **only if** | chỉ khi | The discount applies **only if** you order in bulk. |
| **on condition that** | với điều kiện | She agreed **on condition that** she got a raise. |
| **suppose/supposing** | giả sử như | **Suppose** the deal falls through — what's plan B? |

---

:::tip
**Mẹo làm bài TOEIC:**
- Xác định loại conditional bằng **thì của mệnh đề if**
- **Would KHÔNG đứng trong mệnh đề if**
- **Unless** = if...not (đổi lại để kiểm tra nghĩa)
- Đảo ngữ **Should/Were/Had** = dạng trang trọng của if — hay gặp trong email/văn bản TOEIC
- **Wish + past perfect** = hối tiếc về quá khứ (hay xuất hiện Part 6/7)
:::
""",
    },
    {
        "name": "Passive Voice",
        "slug": "passive-voice",
        "description": "Active to passive transformations across different tenses",
        "summary": """## Câu Bị Động (Passive Voice)

---

## Cấu Trúc Tổng Quát

`S (bị tác động) + be (chia thì) + V3 + (by + tác nhân)`

---

## Bảng Chuyển Đổi Theo Thì

| Thì | Chủ động | Bị động |
|-----|---------|---------|
| Hiện tại đơn | sends | **is/are sent** |
| Hiện tại tiếp diễn | is sending | **is/are being sent** |
| Hiện tại hoàn thành | has sent | **has/have been sent** |
| Quá khứ đơn | sent | **was/were sent** |
| Quá khứ tiếp diễn | was sending | **was/were being sent** |
| Quá khứ hoàn thành | had sent | **had been sent** |
| Tương lai đơn | will send | **will be sent** |
| Tương lai hoàn thành | will have sent | **will have been sent** |
| Modal | should send | **should be sent** |
| Modal perfect | should have sent | **should have been sent** |
| be going to | is going to send | **is going to be sent** |

:::example
- Active: The committee **reviews** all applications.
- Passive: All applications **are reviewed** by the committee.

- Active: They **have completed** the project.
- Passive: The project **has been completed**.

- Active: Management **will announce** the results next week.
- Passive: The results **will be announced** next week.
:::

---

## Khi Nào Dùng Câu Bị Động?

- Không biết hoặc không cần nêu chủ thể hành động
- Muốn nhấn mạnh đối tượng bị tác động
- Văn phong trang trọng: báo cáo, khoa học, kinh doanh
- Chủ thể là "people" hoặc chung chung

:::example
- **The annual report was published** last week. *(không cần nêu ai)*
- **Mistakes were made** during the rollout. *(tránh đổ lỗi)*
- **English is spoken** worldwide.
:::

---

## Câu Bị Động Với Hai Tân Ngữ

:::example
Active: The HR team **gave** her a promotion.
- Passive 1: **She was given** a promotion by the HR team. *(tân ngữ gián tiếp lên đầu)*
- Passive 2: **A promotion was given to her** by the HR team. *(tân ngữ trực tiếp lên đầu)*
:::

*Động từ có hai tân ngữ:* give, send, offer, award, show, tell, pay, lend, teach, grant

---

## Câu Bị Động Với Động Từ Tường Thuật

**Cấu trúc 1:** `It + is/are + said/believed/reported/known/expected + that + clause`

**Cấu trúc 2:** `S + is/are + said/believed/reported/known/expected + to + V`

:::example
- It is **said that** the company will merge.
  → The company **is said to** be merging.

- It is **believed that** profits will increase.
  → Profits **are believed to** increase.

- It is **expected that** she will be promoted.
  → She **is expected to** be promoted.

- It is **reported that** the CEO has resigned.
  → The CEO **is reported to** have resigned.
:::

*Động từ thường dùng:* say, believe, report, know, expect, consider, think, claim, allege, estimate

---

## Causative Have / Get

Nhờ/thuê người khác làm việc gì:

| Cấu trúc | Nghĩa | Ví dụ |
|----------|-------|-------|
| **have + O + V3** | nhờ/thuê làm | We **had** the report **reviewed** by an expert. |
| **get + O + V3** | nhờ/thuê làm (thông dụng) | She **got** the contract **signed** before the meeting. |
| **have + O + V** (bare) | bảo ai làm gì | The manager **had** the team **submit** the report. |
| **get + O + to V** | thuyết phục ai làm gì | She **got** the client **to sign** the contract. |

---

## Get-Passive (Văn Nói / Thông Dụng)

**Cấu trúc:** `S + get + V3`

:::example
- The shipment **got delayed** due to bad weather.
- He **got promoted** after just one year.
- The contract **got signed** yesterday.
- She **got fired** without notice.
:::

---

## Bị Động Với Giới Từ

Một số động từ khi bị động vẫn giữ giới từ:

:::example
- They **looked after** the visitors. → The visitors **were looked after**.
- We **deal with** complaints immediately. → Complaints **are dealt with** immediately.
- She **was satisfied with** the results. *(tính từ + giới từ)*
:::

---

:::tip
**Mẹo làm bài TOEIC:**
- Blank sau chủ ngữ + không có tân ngữ → thường là **passive** (be + V3)
- Chủ ngữ là người/vật bị tác động → passive
- Chia đúng **be** theo thì: is/are, was/were, will be, has/have been, had been...
- **by** thường bỏ khi tác nhân là people/someone/they (không cần thiết)
- Phân biệt: **interested** (bị động — cảm xúc) vs **interesting** (chủ động — gây cảm xúc)
:::
""",
    },
    {
        "name": "Relative Clauses",
        "slug": "relative-clauses",
        "description": "Who, which, that, whose in defining and non-defining clauses",
        "summary": """## Mệnh Đề Quan Hệ (Relative Clauses)

---

## Các Đại Từ & Trạng Từ Quan Hệ

| Từ | Thay thế | Chức năng | Ví dụ |
|----|---------|----------|-------|
| **who** | người | chủ ngữ | The employee **who** won the award... |
| **whom** | người | tân ngữ | The client **whom** we met yesterday... |
| **whose** | người/vật | sở hữu | The manager **whose** team exceeded targets... |
| **which** | vật/sự vật | chủ ngữ/tân ngữ | The report **which** was submitted... |
| **that** | người/vật | chủ ngữ/tân ngữ (defining only) | The file **that** you requested... |
| **where** | nơi chốn | trạng ngữ | The building **where** we work... |
| **when** | thời gian | trạng ngữ | The day **when** she was hired... |
| **why** | lý do | trạng ngữ | The reason **why** sales declined... |

---

## 1. Mệnh Đề Quan Hệ Xác Định (Defining Relative Clauses)

- **Không có dấu phẩy** — thông tin bắt buộc, thiếu đi câu mất nghĩa
- Có thể dùng **that** thay cho who/which
- Có thể **bỏ** đại từ quan hệ nếu nó là **tân ngữ**

:::example
- The candidate **who/that spoke** the most clearly got the job.
- The proposal **(that/which) we submitted** last week was approved. *(that/which có thể bỏ)*
- The software **that automates** invoicing saves hours each week.
:::

---

## 2. Mệnh Đề Quan Hệ Không Xác Định (Non-defining Relative Clauses)

- **Có dấu phẩy** — thông tin bổ sung, bỏ đi câu vẫn hiểu
- **KHÔNG dùng "that"**
- **KHÔNG bỏ** đại từ quan hệ

:::example
- Ms. Kim, **who joined last month**, has already impressed everyone.
- The new office, **which is located in District 1**, can accommodate 200 staff.
- The annual bonus, **which was announced yesterday**, will be paid in December.
:::

---

## 3. "That" vs "Which" — Khi Nào Dùng?

| | **that** | **which** |
|-|---------|---------|
| Mệnh đề xác định | ✓ Dùng được | ✓ Dùng được |
| Mệnh đề không xác định | ✗ Không dùng | ✓ Phải dùng |
| Sau dấu phẩy | ✗ Không dùng | ✓ Phải dùng |
| Sau giới từ | ✗ Không dùng | ✓ in which, of which |
| Sau: everything, all, only, first, superlative | ✓ Ưu tiên | ✗ Ít dùng |

---

## 4. Rút Gọn Mệnh Đề Quan Hệ (Reduced Relative Clauses)

> **Điều kiện:** Chủ ngữ của relative clause phải **trùng** với antecedent.

### Rút gọn → V-ing (Active)

```
who/which + V (chủ động) → V-ing
```

:::example
- Employees **who work** overtime → Employees **working** overtime
- The man **who is standing** there → The man **standing** there
- The manager **who handles** complaints → The manager **handling** complaints
:::

### Rút gọn → V3/ed (Passive)

```
who/which + be + V3 (bị động) → V3
```

:::example
- The contract **that was signed** last week → The contract **signed** last week
- Products **that are manufactured** locally → Products **manufactured** locally
- The man **who was injured** in the accident → The man **injured** in the accident
:::

### Rút gọn → To-infinitive

Sau: **first, last, only, next** + superlative; hoặc diễn tả mục đích/khả năng.

:::example
- She was the first person **who arrived** → She was the first person **to arrive**.
- He is the only one **who knows** → He is the only one **to know**.
- I need someone **who can help** me → I need someone **to help** me.
- We need a room **where we can hold** the meeting → We need a room **to hold** the meeting.
:::

### Rút gọn → Having + V3 (hoàn thành trước)

Khi hành động trong clause xảy ra **trước** hành động câu chính.

:::example
- The man **who had finished** his work left early → **Having finished** his work, the man left early.
- She, **who had lost** her keys, called the locksmith → **Having lost** her keys, she called the locksmith.
:::

---

## 5. "Which" Thay Cho Cả Mệnh Đề

:::example
- He arrived late, **which** made everyone angry.
  ↑ "which" = cả việc anh ấy đến muộn
- She passed the exam, **which** surprised her family.
:::

---

## 6. Mệnh Đề Quan Hệ Với Giới Từ

:::example
- The company **for which** she works is expanding. *(trang trọng)*
  = The company **that she works for**. *(thông thường)*
- The department **in which** I work has 20 employees.
:::

---

## 7. Whoever / Whatever / Whichever

Không cần antecedent đứng trước:

:::example
- **Whoever** comes first will get the prize. *(= Anyone who...)*
- **Whatever** you decide, I'll support you. *(= No matter what...)*
- **Whichever** option you choose, inform us by Friday.
:::

---

:::tip
**Mẹo làm bài TOEIC:**
- Thấy dấu **phẩy + blank + phẩy** → non-defining → chọn who/which, KHÔNG chọn that
- **Whose + N** (không có "the" sau whose)
- Blank sau danh từ: chủ ngữ clause = antecedent + active → V-ing; passive → V3
- **Whom** = who làm tân ngữ, đứng sau giới từ (to whom, for whom)
- Sau **first/last/only/next** → to-infinitive
:::
""",
    },
    {
        "name": "Subject-Verb Agreement",
        "slug": "subject-verb-agreement",
        "description": "Singular and plural agreement including complex subject constructions",
        "summary": """## Sự Hòa Hợp Chủ Ngữ – Động Từ (Subject-Verb Agreement)

---

## Quy Tắc Cơ Bản

- Chủ ngữ **số ít** → động từ **số ít** (thêm -s/-es, hoặc is/was/has)
- Chủ ngữ **số nhiều** → động từ **số nhiều** (không thêm -s, hoặc are/were/have)

---

## Các Trường Hợp Đặc Biệt

### 1. Chủ Ngữ Ghép Nối Bằng AND → Số Nhiều

:::example
- The CEO and the CFO **are** attending the conference.
- Experience and dedication **are** required for this position.
:::

:::warning
**Ngoại lệ:** Hai danh từ chỉ một người/vật hoặc một khái niệm → số ít:
- The founder and CEO **is** John Smith. *(một người)*
- Bread and butter **is** all I need. *(một món)*
- Every man and woman **is** invited. *("every" → số ít dù có "and")*
:::

---

### 2. Either...Or / Neither...Nor / Or

Động từ chia theo **danh từ gần nhất**:

:::example
- Either the manager or the **employees are** responsible.
- Either the **employees** or the manager **is** responsible.
- Neither the director nor the **assistants were** informed.
- Neither he nor **I am** going.
:::

---

### 3. Danh Từ Tập Thể (Collective Nouns) → Số Ít (TOEIC)

:::example
- The **committee has** decided to postpone the vote.
- The **team is** working on the new project.
- The **staff is** required to complete the training.
- The **board has** approved the budget.
:::

*Common collective nouns:* team, committee, board, staff, management, department, crew, audience, group, company, government

---

### 4. Danh Từ Trông Như Số Nhiều Nhưng Là Số Ít

:::example
- The **news is** encouraging.
- **Economics is** a required subject.
- **Mathematics is** required.
- The **United States is** a major trading partner.
- **Headquarters is** located in Singapore.
:::

*Danh từ luôn số ít:* news, economics, mathematics, physics, statistics (môn học), the United States, the Netherlands, measles, mumps

*Danh từ luôn số nhiều:* scissors, pants, glasses, jeans, goods, earnings, savings, belongings, people, police, cattle

---

### 5. A Number Of vs The Number Of

| Cụm | Động từ | Ví dụ |
|-----|---------|-------|
| **A number of** + N plural | **Số nhiều** | A number of employees **are** absent. |
| **The number of** + N plural | **Số ít** | The number of applications **has** increased. |
| **A variety of** + N plural | **Số nhiều** | A variety of options **are** available. |
| **The majority of** + N plural | **Số nhiều** | The majority of clients **prefer** online billing. |

:::tip
**Nhớ:** A number → nhiều → plural | The number → một con số → singular
:::

---

### 6. Phần Trăm / Phân Số / Some / All / Most / Half

Chia theo **danh từ theo sau "of"**:

:::example
- 50% of the **budget has** been used. *(budget = singular)*
- 50% of the **employees have** left. *(employees = plural)*
- All of the **water is** clean.
- All of the **students are** present.
- Most of the **work is** done.
- Half of the **cake was** eaten.
:::

---

### 7. Chủ Ngữ Bị Tách Bởi Cụm Từ

Bỏ qua cụm **chen giữa** chủ ngữ và động từ:

*along with, as well as, together with, in addition to, including, except, rather than*

:::example
- The CEO, **along with** his assistants, **is** attending the summit.
- The report, **including all appendices**, **was** submitted on time.
- The quality of the products **is** high. *(chia theo "quality")*
- A list of items **was** submitted.
:::

---

### 8. Each / Every / Either / Neither + N → Số Ít

:::example
- **Each** department **has** a separate budget.
- **Every** employee **is** required to sign the form.
- **Either** option **is** acceptable.
- **Neither** candidate **was** selected.
:::

---

### 9. Đại Từ Bất Định → Số Ít

*everyone, everybody, everything, someone, somebody, something, anyone, anybody, anything, no one, nobody, nothing*

:::example
- **Everyone** in the meeting **was** asked to contribute.
- **Nobody** from the sales team **has** responded yet.
- **Each** of the proposals **has** its own merits.
:::

---

### 10. There Is / There Are

Chia theo danh từ **đứng sau**:

:::example
- There **is** a problem.
- There **are** several problems.
- There **is** a book and a pen on the desk. *(gần "book" → is)*
:::

---

### 11. Mệnh Đề / Danh Động Từ Làm Subject → Số Ít

:::example
- **What he said is** true.
- **That she resigned was** a surprise.
- **Working overtime is** exhausting.
- **To err is** human.
:::

---

### 12. Khoảng Cách, Thời Gian, Tiền, Số Lượng → Số Ít

:::example
- Ten miles **is** a long distance.
- Five years **is** too long to wait.
- $500 **was** spent on supplies.
- Three hours **is** enough time.
:::

---

:::tip
**Mẹo làm bài TOEIC:**
- Xác định **chủ ngữ thật** = bỏ qua mọi cụm bổ nghĩa giữa chủ ngữ và động từ
- Collective noun (team, staff, committee) → số ít trong TOEIC
- **a number of** → plural | **the number of** → singular (học thuộc)
- Danh từ kết thúc -s không phải lúc nào cũng số nhiều (news, mathematics, economics)
- Phần trăm / Half / Most / All + **of** + N → chia theo N sau "of"
- Mệnh đề / Gerund làm subject → luôn singular
:::
""",
    },
    {
        "name": "Gerunds & Infinitives",
        "slug": "gerunds-infinitives",
        "description": "When to use -ing forms vs. to + verb after verbs and prepositions",
        "summary": """## Danh Động Từ & Động Từ Nguyên Mẫu (Gerunds & Infinitives)

---

## 1. Danh Động Từ (Gerund = V-ing)

### Chức năng

| Vai trò | Ví dụ |
|---------|-------|
| **Làm chủ ngữ** | **Managing** a team requires strong communication. |
| **Làm tân ngữ** | She enjoys **networking** at industry events. |
| **Sau giới từ** | He is responsible **for overseeing** the project. |
| **Sau be worth / be no use** | This opportunity is worth **considering**. |

### Động Từ + Gerund (V-ing)

> enjoy, finish, avoid, consider, suggest, recommend, keep, mind, practice, delay, postpone, deny, admit, risk, involve, miss, appreciate, resist, imagine, dislike, can't help, can't stand, give up, put off, look forward to, be used to, get used to, object to, insist on, succeed in, be worth, result in, prevent (from), prohibit (from), discourage (from)

:::example
- The board **suggested implementing** a new policy.
- She **avoids making** decisions without data.
- I **look forward to meeting** you next week. *(to là giới từ)*
- He **finished reviewing** the contracts.
- We **succeeded in reducing** costs by 20%.
:::

---

## 2. Động Từ Nguyên Mẫu (Infinitive = To + V)

### Chức năng

| Vai trò | Ví dụ |
|---------|-------|
| **Làm chủ ngữ** | **To succeed** in business requires perseverance. |
| **Diễn tả mục đích** | She traveled **to attend** the conference. |
| **Sau tính từ** | We are pleased **to announce** the results. |
| **Sau it is + adj** | It is important **to verify** all data. |
| **Sau enough / too** | He is experienced enough **to lead** the team. |

### Động Từ + To-Infinitive

> want, need, hope, plan, decide, agree, refuse, offer, promise, expect, attempt, manage, tend, fail, seem, appear, arrange, choose, prepare, intend, afford, demand, deserve, pretend, wish, claim, threaten

:::example
- The company **decided to restructure** its operations.
- She **managed to complete** the report before the deadline.
- Management **agreed to review** the compensation package.
- We **expect to launch** the product next quarter.
:::

### Động Từ + O + To-Infinitive

> ask, tell, advise, encourage, allow, require, force, invite, remind, warn, expect, want, need, persuade, enable, teach, permit

:::example
- Management **asked employees to submit** feedback.
- The policy **requires all staff to wear** ID badges.
- She **encouraged the team to take** initiative.
:::

---

## 3. Động Từ Dùng Cả Hai (Nghĩa Thay Đổi)

| Động từ | + Gerund | + Infinitive |
|---------|---------|-------------|
| **remember** | nhớ lại việc đã làm | nhớ phải làm việc gì |
| **forget** | quên việc đã làm | quên phải làm việc gì |
| **stop** | dừng hẳn việc đang làm | dừng lại để làm việc khác |
| **try** | thử xem kết quả | cố gắng đạt được mục tiêu |
| **regret** | hối tiếc vì đã làm | tiếc phải thông báo |
| **mean** | đồng nghĩa với | có ý định |

:::example
- I remember **meeting** her at the conference. *(đã gặp rồi)*
- Remember **to submit** the form before Friday. *(nhớ làm)*
- He stopped **smoking**. *(bỏ hẳn)*
- He stopped **to check** his phone. *(dừng để làm việc khác)*
- We regret **to inform** you that your application was unsuccessful. *(thông báo chính thức)*
- She regrets **not taking** the opportunity. *(hối tiếc)*
- Expanding **means hiring** more staff. *(đồng nghĩa với)*
- I **mean to** finish this today. *(có ý định)*
:::

---

## 4. Động Từ Dùng Cả Hai (Nghĩa Không Đổi)

> begin, start, continue, like, love, hate, prefer

:::example
- She **likes to work / working** independently.
- The meeting **continued to run / running** over time.
:::

:::warning
Sau **would like/love/prefer/hate** → luôn dùng **to-infinitive**:
- I **would like to attend** the conference. *(không phải attending)*
:::

---

## 5. Cấu Trúc Đặc Biệt: V nguyên mẫu KHÔNG TO (Bare Infinitive)

| Sau | Ví dụ |
|-----|-------|
| **make / let** | The update **makes** the system **run** faster. Please **let** me **know**. |
| **help** (có thể có to) | This tool **helps** employees **track** / **to track** progress. |
| **had better** | You **had better respond** quickly. |
| **would rather** | I **would rather work** from home. |
| Modal verbs | She **can solve** the problem. |

---

## 6. Too / Enough + Infinitive

```
too + adj/adv + to V     = quá...để không thể
adj/adv + enough + to V  = đủ...để có thể
```

:::example
- The report is **too long to read** in one sitting.
- She is **experienced enough to handle** the project independently.
- He was **not old enough to apply** for the senior position.
:::

---

## 7. Sau Giới Từ → Luôn V-ing

:::example
- She left **without saying** goodbye.
- He is good **at presenting** ideas clearly.
- I'm interested **in joining** the team.
- **Upon receiving** the email, she called immediately.
  *(upon + V-ing = ngay khi...)*
:::

---

:::tip
**Mẹo làm bài TOEIC:**
- Sau **giới từ** (in, on, of, for, about, at, without, upon...) → luôn **V-ing**
- **look forward to + V-ing** (to = giới từ, KHÔNG phải to-infinitive)
- **be used to + V-ing** (quen với) ≠ **used to + V** (thường làm trước đây)
- **make/let** → V bare (không to) | **allow/ask/tell/want/require** → to + V
- **would like/love/prefer** → to-infinitive (không phải V-ing)
- Blank sau giới từ → V-ing; blank sau modal → V bare
:::
""",
    },
    {
        "name": "Comparatives & Superlatives",
        "slug": "comparatives-superlatives",
        "description": "Comparing adjectives and adverbs: more/most, -er/-est, as...as",
        "summary": """## So Sánh (Comparatives & Superlatives)

---

## 1. So Sánh Hơn (Comparative)

### Quy Tắc Thêm Đuôi

| Quy tắc | Ví dụ |
|---------|-------|
| Ngắn → thêm **-er** | fast → faster, hard → harder |
| Kết thúc **-e** → thêm **-r** | large → larger, safe → safer |
| Phụ âm + nguyên âm + phụ âm → nhân đôi | big → bigger, hot → hotter |
| Kết thúc **-y** → **-ier** | easy → easier, busy → busier |
| Dài (≥3 âm tiết) → **more/less** | more efficient, less expensive |

**Cấu trúc:** `S + V + adj-er / more + adj + than + N/pronoun`

:::example
- This quarter's results are **better than** last year's.
- The new system is **more efficient than** the old one.
- Remote work is **becoming more common than** before.
:::

---

## 2. So Sánh Nhất (Superlative)

**Cấu trúc:** `the + adj-est / the most + adj + (in/of + N)`

:::example
- She is **the most experienced** candidate in the pool.
- This is **the highest** revenue the company has ever achieved.
- It is **the least expensive** option available.
:::

:::warning
Sau superlative thường dùng **Present Perfect**:
- This is **the best** report she **has ever written**.
- It is **the most successful** campaign we **have ever run**.
:::

---

## 3. So Sánh Ngang Bằng

| Cấu trúc | Ví dụ |
|----------|-------|
| **as + adj/adv + as** | This report is **as detailed as** the previous one. |
| **not as/so + adj + as** | The new office is **not as large as** we hoped. |
| **the same + N + as** | He earns **the same salary as** his colleagues. |
| **similar to** | The process is **similar to** what we used before. |
| **equal to** | The bonus is **equal to** one month's salary. |

---

## 4. Dạng Bất Quy Tắc

| Gốc | Comparative | Superlative |
|-----|-------------|-------------|
| good / well | better | the best |
| bad / badly | worse | the worst |
| many / much | more | the most |
| little (lượng) | less | the least |
| few (số) | fewer | the fewest |
| far | farther (khoảng cách) / further (mức độ) | the farthest / furthest |
| late | later (thời gian) / latter (thứ tự) | the latest (mới nhất) / last (cuối) |
| old | older / elder (người trong gia đình) | the oldest / eldest |

---

## 5. Từ Bổ Nghĩa So Sánh (Modifiers)

| Mức độ | Từ bổ nghĩa | Ví dụ |
|--------|------------|-------|
| Hơn nhiều | **much, far, a lot, significantly, considerably** | **far** better, **much** more efficient |
| Hơn một chút | **a little, slightly, somewhat** | **slightly** higher, **a little** faster |
| Bằng nhau chính xác | **just as** | **just as** important |

:::example
- The new model is **significantly more** energy-efficient.
- Sales are **slightly higher** than expected.
- Results were **far better** than last year.
:::

---

## 6. Cấu Trúc Nâng Cao

### The + comparative, the + comparative

:::example
- **The more** you practice, **the better** your score will be.
- **The earlier** we start, **the sooner** we'll finish.
- **The higher** the quality, **the more** customers will trust us.
:::

### Comparative + and + comparative (ngày càng...)

:::example
- Competition is becoming **more and more** intense.
- The workload is growing **heavier and heavier**.
- Prices are getting **lower and lower**.
:::

### Multiplier + as...as / times more than

:::example
- The new warehouse is **twice as large as** the old one.
- Revenue is **three times higher than** last year.
- This model is **50% more efficient** than its predecessor.
:::

---

## 7. Tính Từ Đặc Biệt: Dùng "to" Thay Vì "than"

| Từ | Cấu trúc đúng | Cấu trúc sai |
|----|--------------|-------------|
| superior | superior **to** | ~~superior than~~ |
| inferior | inferior **to** | ~~inferior than~~ |
| senior | senior **to** | ~~senior than~~ |
| junior | junior **to** | ~~junior than~~ |
| prior | prior **to** | ~~prior than~~ |
| preferable | preferable **to** | ~~preferable than~~ |

:::example
- This product is **superior to** the competitor's version.
- She is **senior to** him by three years.
- Online payment is **preferable to** cash transactions.
:::

---

## 8. Các Cấu Trúc Khác

### No + comparative + than (không...hơn)
:::example
- The report is **no longer than** expected.
- The result is **no better than** before.
:::

### As...as possible
:::example
- Please respond **as soon as possible**.
- Complete the task **as efficiently as possible**.
:::

### One of the + superlative + plural noun
:::example
- She is **one of the most experienced** managers in the company.
:::

---

:::tip
**Mẹo làm bài TOEIC:**
- Sau **than** → đại từ tân ngữ hoặc mệnh đề: better than **him** / better than **he does**
- **superior/inferior/senior/junior/prior/preferable** + **to** (không dùng than)
- **farther** = khoảng cách vật lý | **further** = mức độ, thêm vào (further discussion)
- **latest** = mới nhất (vẫn còn thêm) | **last** = cuối cùng (kết thúc)
- Superlative + Present Perfect: "the best...I have ever seen"
- Modifiers: much/far (hơn nhiều) | a little/slightly (hơn một chút)
:::
""",
    },
    {
        "name": "Conjunctions & Connectors",
        "slug": "conjunctions-connectors",
        "description": "Coordinating, subordinating, and correlative conjunctions; discourse markers",
        "summary": """## Liên Từ & Từ Nối (Conjunctions & Connectors)

---

## 1. Liên Từ Kết Hợp (Coordinating Conjunctions — FANBOYS)

Nối hai **mệnh đề độc lập** — phải có dấu phẩy trước liên từ.

| Liên từ | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| **and** | thêm vào | Sales grew, **and** profit margins improved. |
| **but** | tương phản | The plan was approved, **but** funding was limited. |
| **or** | lựa chọn | We can delay, **or** we can proceed as planned. |
| **so** | kết quả | The deadline was tight, **so** we worked overtime. |
| **yet** | tương phản bất ngờ | The task was difficult, **yet** the team completed it. |
| **for** | nguyên nhân (trang trọng) | He resigned, **for** he was unhappy. |
| **nor** | phủ định thêm | She didn't attend, **nor** did she send a representative. |

---

## 2. Liên Từ Phụ Thuộc (Subordinating Conjunctions)

Nối mệnh đề phụ vào mệnh đề chính. Mệnh đề phụ không đứng riêng.

### Thời gian
> when, while, before, after, until/till, as soon as, once, since, whenever, by the time, as

:::example
- **After** the contract was signed, the project began immediately.
- **As soon as** the manager approves it, we'll proceed.
- **By the time** the team arrived, the meeting had ended.
- **While** he was presenting, the fire alarm went off.
:::

### Nguyên nhân
> because, since, as, now that, seeing that

:::example
- **Because** the budget was cut, we had to revise the plan.
- **Since** we've already invested heavily, we should continue.
- **Now that** the merger is complete, we can expand.
:::

### Mục đích
> so that, in order that

:::example
- We streamlined the process **so that** employees could work more efficiently.
- Meetings were shortened **in order that** staff could focus on core tasks.
:::

### Kết quả
> so...that, such...that

:::example
- The demand was **so high that** we had to hire additional staff.
- It was **such a successful** campaign **that** we extended it.
- She spoke **so clearly that** everyone understood immediately.
:::

:::tip
**so + adj/adv + that** | **such + (a/an) + adj + noun + that**
- so **quickly** that | such **a quick** decision that
:::

### Nhượng bộ
> although, though, even though, while, whereas, even if

:::example
- **Although** the market was challenging, we exceeded our targets.
- **Even though** costs rose, we maintained profitability.
- Sales increased **whereas** expenses remained flat. *(tương phản)*
:::

### Điều kiện
> if, unless, provided that, as long as, in case, only if, on condition that

### So sánh
> as...as, than, the more...the more

---

## 3. Liên Từ Tương Quan (Correlative Conjunctions)

Luôn đi theo **cặp** — cấu trúc sau mỗi vế phải **song song** (parallel structure).

| Cặp | Ý nghĩa | Ví dụ |
|-----|---------|-------|
| **both...and** | cả hai | **Both** the quality **and** the price are competitive. |
| **either...or** | hoặc...hoặc | We can **either** reduce costs **or** increase revenue. |
| **neither...nor** | không...cũng không | **Neither** the manager **nor** the team was consulted. |
| **not only...but also** | không chỉ...mà còn | The update **not only** improves speed **but also** enhances security. |
| **whether...or** | dù...hay | **Whether** you agree **or** not, the policy stands. |
| **as...as** | ngang bằng | It is **as important as** any other factor. |

:::warning
**Parallel structure** bắt buộc:
- ✅ Both **reducing** costs **and increasing** revenue are priorities.
- ❌ Both **reducing** costs **and to increase** revenue...
:::

---

## 4. Trạng Từ Liên Kết (Conjunctive Adverbs)

Đứng đầu câu sau **; hoặc .** — phải có **dấu phẩy** theo sau.

| Nhóm | Từ nối |
|------|--------|
| Tương phản | **however, nevertheless, nonetheless, on the other hand, in contrast** |
| Kết quả | **therefore, thus, hence, consequently, as a result, accordingly** |
| Bổ sung | **moreover, furthermore, in addition, additionally, besides** |
| Thời gian | **meanwhile, in the meantime, subsequently, afterward** |
| Ví dụ | **for example, for instance, specifically, namely** |
| Tóm tắt | **in conclusion, in summary, overall, in short** |
| Thay thế | **instead, alternatively, otherwise** |
| Tương tự | **similarly, likewise, in the same way** |

:::example
- The project was over budget; **however**, the client was satisfied.
- We improved our processes; **consequently**, productivity increased by 20%.
- The deadline was moved up; **therefore**, we need more resources.
- Sales declined in Q1; **nevertheless**, we maintained market share.
:::

---

## 5. Giới Từ vs Liên Từ (Hay Nhầm Trong TOEIC)

| Ý nghĩa | Liên từ (+ S + V) | Giới từ (+ N/V-ing) |
|---------|------------------|---------------------|
| Dù, mặc dù | although, though, even though | **despite**, **in spite of** |
| Vì | because, since, as | **because of**, **due to**, **owing to**, **on account of** |
| Trong khi | while | **during** |
| Ngay khi | as soon as | **upon** + V-ing |
| Thay vì | instead of (liên từ) | **instead of** + N/V-ing |
| Ngoài ra | besides (liên từ) | **besides** + N/V-ing |

:::example
- **Although** the weather was bad, we proceeded. *(+ clause)*
- **Despite** the bad weather, we proceeded. *(+ noun)*
- **Despite the fact that** the weather was bad, we proceeded. *(+ clause)*

- **Because** costs rose, we revised the budget. *(+ clause)*
- **Because of** / **Due to** rising costs, we revised the budget. *(+ noun)*
:::

---

:::tip
**Mẹo làm bài TOEIC:**
- Blank giữa hai mệnh đề hoàn chỉnh: liên từ (and/but/so) hoặc trạng từ liên kết (however/therefore)
- Blank trước N/V-ing: giới từ (despite/because of/during)
- **Dấu chấm phẩy (;)** → trạng từ liên kết (however/therefore...)
- **Parallel structure** với correlative: both A and B → A và B cùng dạng từ
- **so...that** vs **such...that**: so + adj/adv | such + (a/an +) adj + noun
:::
""",
    },
    {
        "name": "Word Forms",
        "slug": "word-forms",
        "description": "Choosing the correct noun, verb, adjective, or adverb form in context",
        "summary": """## Dạng Từ (Word Forms)

---

## 1. Bốn Loại Từ Chính

| Loại | Câu hỏi | Vị trí | Ví dụ |
|------|---------|--------|-------|
| **Danh từ (Noun)** | Ai? Cái gì? | Chủ ngữ, tân ngữ, sau mạo từ/giới từ | the **manager**, **efficiency**, **approval** |
| **Động từ (Verb)** | Làm gì? | Sau chủ ngữ (vị ngữ) | **manages**, **is improving**, **was approved** |
| **Tính từ (Adjective)** | Như thế nào? | Trước danh từ; sau be/seem/look/become/feel | **efficient** manager, is **professional** |
| **Trạng từ (Adverb)** | Thế nào? Đến mức nào? | Trước V, Adj, Adv khác; cuối câu | works **efficiently**, **highly** qualified |

---

## 2. Hậu Tố Nhận Biết Dạng Từ

### Hậu Tố Danh Từ

| Hậu tố | Ví dụ |
|--------|-------|
| -tion / -sion | information, decision, expansion, promotion |
| -ment | management, development, improvement, achievement |
| -ness | effectiveness, awareness, happiness, willingness |
| -ity / -ty | productivity, quality, responsibility, ability |
| -ance / -ence | performance, confidence, compliance, attendance |
| -er / -or / -ist / -ian | manager, director, analyst, technician |
| -ship | leadership, partnership, membership, ownership |
| -al | proposal, approval, renewal, refusal |
| -ure | procedure, failure, exposure, departure |
| -ry / -ery | delivery, discovery, machinery |
| -age | shortage, storage, coverage, usage |

### Hậu Tố Động Từ

| Hậu tố | Ví dụ |
|--------|-------|
| -ize / -ise | organize, specialize, prioritize, maximize |
| -ify | simplify, clarify, notify, justify |
| -en | strengthen, broaden, tighten, widen |
| -ate | communicate, evaluate, coordinate, negotiate |

### Hậu Tố Tính Từ

| Hậu tố | Ví dụ |
|--------|-------|
| -ful | successful, resourceful, careful, meaningful |
| -less | careless, effortless, groundless, wireless |
| -ous / -ious | ambitious, previous, various, prestigious |
| -al | professional, financial, additional, seasonal |
| -ic | economic, specific, strategic, realistic |
| -ive | effective, competitive, productive, innovative |
| -able / -ible | available, reliable, flexible, responsible |
| -ent / -ant | efficient, significant, relevant, prominent |
| -ary / -ory | necessary, mandatory, regulatory |
| -ing / -ed | interesting/interested, satisfying/satisfied |

### Hậu Tố Trạng Từ → Tính từ + **-ly**

> efficiently, professionally, significantly, increasingly, carefully, thoroughly, promptly, accordingly

:::warning
Trạng từ KHÔNG có -ly: fast, hard, late, early, high, low, well, enough, already
- She works **hard** ≠ She works **hardly** (hardly = hầu như không)
- He arrived **late** ≠ He arrived **lately** (lately = gần đây)
- The plane flew **high** *(adv)* | a **high** mountain *(adj)*
:::

---

## 3. Chiến Lược Xác Định Dạng Từ Trong TOEIC

### Bước 1: Xác định vị trí blank

| Vị trí blank | Dạng từ cần điền |
|-------------|----------------|
| Sau mạo từ (a/an/the) | Noun hoặc Adj + Noun |
| Sau possessive (my/his/our/its) | Noun |
| Sau be/seem/become/feel/look/appear | **Adjective** (KHÔNG phải adverb) |
| Sau verb thường (bổ nghĩa động từ) | **Adverb** |
| Trước noun (bổ nghĩa danh từ) | **Adjective** |
| Làm chủ ngữ / tân ngữ câu | Noun |
| Sau to (infinitive) | Verb |
| Bổ nghĩa adjective / adverb khác | Adverb |

### Bước 2: Nhận diện gốc từ, thêm hậu tố

:::example
- "Her ______ (innovate) approach" → trước N → Adj → **innovative**
- "The team works ______ (efficient)" → sau V → Adv → **efficiently**
- "She received a ______ (promote)" → sau "a" → N → **promotion**
- "We need to ______ (strong) our brand" → sau to → V → **strengthen**
- "The results were ______ (disappoint)" → sau be → Adj → **disappointing** hoặc **disappointing**?
  → Kết quả GÂY thất vọng → **disappointing**
:::

---

## 4. Phân Biệt -ED và -ING (Participial Adjectives)

| Dạng | Ý nghĩa | Chủ thể |
|------|---------|---------|
| **-ING** | GÂY ra cảm xúc / đặc tính vốn có | Vật/tình huống |
| **-ED** | CẢM THẤY / bị tác động | Người (nhận cảm xúc) |

:::example
- The presentation was **boring**. → presentation gây chán
- The audience was **bored**. → khán giả cảm thấy chán

- The news is **encouraging**. → tin tức gây khích lệ
- She is **encouraged** by the news. → cô ấy được khích lệ

- It was a **tiring** trip. → chuyến đi gây mệt
- I am **tired** after the trip. → tôi cảm thấy mệt
:::

*Cặp thông dụng:* interesting/interested | exciting/excited | satisfying/satisfied | confusing/confused | surprising/surprised | exhausting/exhausted | motivating/motivated | disappointing/disappointed | overwhelming/overwhelmed

---

## 5. Gia Đình Từ Thông Dụng Trong TOEIC

| Gốc | Noun | Verb | Adjective | Adverb |
|-----|------|------|-----------|--------|
| effect | effect | affect | effective/affected | effectively |
| produce | product/production/productivity | produce | productive | productively |
| manage | management/manager | manage | managerial | — |
| approve | approval | approve | approved/approving | approvingly |
| require | requirement | require | required/requisite | — |
| qualify | qualification | qualify | qualified | — |
| compete | competition/competitor | compete | competitive | competitively |
| perform | performance | perform | performing | — |
| employ | employment/employee/employer | employ | employed/unemployed | — |
| promote | promotion | promote | promotional | promotionally |

---

## 6. Danh Từ Ghép & Tính Từ Ghép Thông Dụng

| Dạng | Ví dụ |
|------|-------|
| N + N | **budget** approval, **sales** report, **job** opening |
| Adj + N | **annual** report, **quarterly** earnings, **senior** management |
| V-ing + N | **marketing** strategy, **training** program, **accounting** department |
| V-ed + N | **experienced** staff, **required** documents |

---

:::tip
**Mẹo làm bài TOEIC:**
- Blank sau **be/seem/become/feel** → **tính từ** (KHÔNG phải trạng từ)
- Blank bổ nghĩa **cả câu hoặc động từ** → **trạng từ** (-ly)
- **hardly/lately/highly/nearly** khác hoàn toàn nghĩa với **hard/late/high/near**
- Phân biệt -ing/-ed: ai/cái gì GÂY ra → -ING; ai/cái gì CẢM THẤY → -ED
- Sau giới từ → **danh từ hoặc V-ing** (không phải tính từ)
:::
""",
    },
]


async def seed():
    async with AsyncSessionLocal() as db:
        for topic_data in TOPICS:
            result = await db.execute(
                select(GrammarTopic).where(GrammarTopic.slug == topic_data["slug"])
            )
            existing = result.scalar_one_or_none()
            if existing:
                # Always update summary to latest content
                existing.summary = topic_data["summary"]
                print(f"  update: {topic_data['name']}")
            else:
                topic = GrammarTopic(**topic_data)
                db.add(topic)
                print(f"  add:    {topic_data['name']}")

        await db.commit()
        print("Seeding complete.")


if __name__ == "__main__":
    asyncio.run(seed())
