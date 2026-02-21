"""
One-time script: update the Articles topic summary with content crawled from
https://zim.vn/cach-dung-a-an-the
"""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.grammar_topic import GrammarTopic

ARTICLES_SUMMARY = """## Mạo Từ Trong Tiếng Anh (Articles: A, An, The)

> Mạo từ (articles) là từ hạn định đứng trước danh từ, báo hiệu danh từ đó đã được xác định hay chưa. Tiếng Anh có 3 mạo từ: **a**, **an** và **the**.

---

## 1. Mạo Từ Không Xác Định: A / AN

Dùng trước danh từ **đếm được số ít** khi danh từ đó chưa được xác định cụ thể.

:::warning
**Quy tắc vàng:** Chọn A hay AN dựa vào **âm thanh phát âm** của từ tiếp theo, KHÔNG dựa vào chữ cái đầu.
:::

| Mạo từ | Khi nào dùng | Ví dụ |
|--------|-------------|-------|
| **a** | Trước âm **phụ âm** | a book, a car, a table, a dog |
| **an** | Trước âm **nguyên âm** | an apple, an egg, an umbrella |

### Các trường hợp dễ nhầm:

| Từ | Phiên âm | Dùng | Lý do |
|----|---------|------|-------|
| university | /ˌjuː.nɪˈvɜː.sə.ti/ | **a** university | Bắt đầu bằng âm /j/ (phụ âm) |
| European | /ˌjʊə.rəˈpiː.ən/ | **a** European | Bắt đầu bằng âm /j/ (phụ âm) |
| umbrella | /ʌmˈbrel.ə/ | **an** umbrella | Bắt đầu bằng âm /ʌ/ (nguyên âm) |
| hour | /aʊər/ | **an** hour | "h" câm, bắt đầu bằng âm /aʊ/ |
| honor | /ˈɒn.ər/ | **an** honor | "h" câm, bắt đầu bằng âm /ɒ/ |
| honest | /ˈɒn.ɪst/ | **an** honest | "h" câm |
| MBA | /ˌem.biːˈeɪ/ | **an** MBA | Chữ M đọc là /em/ (nguyên âm) |
| FBI | /ˌef.biːˈaɪ/ | **an** FBI agent | Chữ F đọc là /ef/ (nguyên âm) |
| unique | /juːˈniːk/ | **a** unique | Bắt đầu bằng âm /j/ (phụ âm) |
| one-time | /wʌn/ | **a** one-time | Bắt đầu bằng âm /w/ (phụ âm) |

### Khi nào dùng A/AN:

**1. Đề cập lần đầu — người nghe chưa biết:**
:::example
- I met **a** girl yesterday. **The** girl wore a beautiful dress.
- She is looking for **a** new job in marketing.
- We need **an** experienced developer for the project.
:::

**2. Nghề nghiệp, chức danh:**
:::example
- She is **an** engineer at Samsung.
- He works as **a** project manager.
- My sister is **a** doctor.
:::

**3. Mang nghĩa "một" (số lượng):**
:::example
- Please give me **a** moment to think.
- I need **a** pen and **an** eraser.
:::

**4. Trong các cụm cố định:**
:::example
- What **a** great presentation! *(What + a/an + adj + N)*
- Such **an** inspiring speech! *(Such + a/an + adj + N)*
- It was quite **a** challenge. *(quite/rather + a/an)*
:::

---

## 2. Mạo Từ Xác Định: THE

Dùng khi **cả người nói lẫn người nghe đều biết** danh từ đó là cái gì.

:::tip
**Câu hỏi thần kỳ:** *"Người nghe có biết tôi đang nói về cái gì không?"*
- Có → dùng **the**
- Không → dùng **a/an** (nếu đếm được, số ít) hoặc không dùng mạo từ
:::

### 13 Trường Hợp Dùng THE

**1. Danh từ duy nhất trên thế giới:**
:::example
- **The** sun rises in the east and sets in the west.
- **The** moon is full tonight.
- **The** earth orbits the sun every 365 days.
- **The** sky is clear today.
:::

**2. So sánh nhất:**
:::example
- He is **the** tallest person in the office.
- This is **the** most innovative product we have ever launched.
- She is **the** best candidate for the position.
:::

**3. Danh từ đã xác định theo ngữ cảnh (cả hai bên đều biết):**
:::example
- Could you pass me **the** salt? *(muối trên bàn ăn — cả hai đều biết)*
- Please close **the** door. *(cánh cửa trong phòng)*
- **The** manager wants to see you. *(người quản lý của chúng ta)*
:::

**4. Danh từ đã được nhắc đến trước đó:**
:::example
- I met **a** girl yesterday. **The** girl wore a beautiful dress.
- We received **a** proposal. **The** proposal looks very promising.
:::

**5. Tính từ đại diện cho nhóm người:**
:::example
- Many charities raise funds for **the** poor. *(người nghèo nói chung)*
- **The** elderly need special care during winter.
- **The** unemployed receive government support.
:::

**6. Nhạc cụ:**
:::example
- I'm learning to play **the** piano.
- She plays **the** violin in a chamber orchestra.
- He is very good at **the** guitar.
:::

**7. Danh từ riêng có nhiều thành phần hoặc mang tên chung:**
:::example
- **The** United States of America
- **The** United Kingdom
- **The** European Union
- **The** Philippines *(quần đảo)*
- **The** Netherlands
:::

**8. Tên báo, tạp chí nổi tiếng:**
:::example
- **The** Times, **The** Washington Post, **The** Economist
:::

**9. Công trình kiến trúc, tác phẩm nghệ thuật nổi tiếng:**
:::example
- **The** Empire State Building
- **The** Eiffel Tower
- **The** Mona Lisa
- **The** Great Wall
:::

**10. Dãy núi, quần đảo, đại dương, sông lớn:**
:::example
- **The** Himalayas, **The** Alps *(dãy núi)*
- **The** Pacific Ocean, **The** Atlantic *(đại dương)*
- **The** Mekong River, **The** Amazon *(sông)*
- **The** Hawaiian Islands *(quần đảo)*
:::

**11. Tên họ ở dạng số nhiều (chỉ cả gia đình):**
:::example
- **The** Obamas visited France last summer.
- **The** Smiths are our neighbors.
:::

**12. Số thứ tự:**
:::example
- She was **the** first employee to be promoted.
- This is **the** second time we've met.
- **The** last item on the agenda is budget review.
:::

**13. Danh từ số ít đại diện cho cả loài:**
:::example
- **The** dog is known for its loyalty.
- **The** computer has changed modern life.
:::

---

## 3. Không Dùng Mạo Từ (Zero Article)

| Trường hợp | Ví dụ |
|-----------|-------|
| **Bữa ăn** | We have **lunch** at noon. / after **breakfast** |
| **Ngôn ngữ** | I learned **English**. / She speaks **French**. |
| **Môn thể thao** | We play **volleyball**. / He loves **tennis**. |
| **Tên riêng** (người, công ty, quốc gia) | **Taylor Swift** is famous. / **Vietnam** is beautiful. |
| **Danh từ số nhiều mang nghĩa chung** | I like **apples**. / **Employees** need training. |
| **Danh từ không đếm được mang nghĩa chung** | **Water** is essential. / **Information** is power. |
| **Học thuật, chuyên ngành** | She studies **medicine**. / He majors in **economics**. |
| **Phương tiện đi lại (by + …)** | travel by **car**, go by **train**, fly by **plane** |
| **Địa điểm mang chức năng** (không phải tòa nhà) | go to **school** (học), go to **hospital** (nhập viện) |

:::warning
**Phân biệt quan trọng:**
- go to **school** *(học sinh đi học)* ≠ go to **the school** *(đến tòa nhà trường)*
- go to **hospital** *(nhập viện điều trị — BrE)* ≠ go to **the hospital** *(thăm bệnh nhân)*
- in **prison** *(đang bị giam)* ≠ in **the prison** *(trong tòa nhà nhà tù)*
:::

---

## 4. Bốn Lỗi Thường Gặp

**Lỗi 1: Nhầm A/AN theo chữ cái thay vì phát âm**
:::example
- ❌ a umbrella, a hour, a honest man
- ✅ **an** umbrella, **an** hour, **an** honest man
- ❌ an university, an European country
- ✅ **a** university, **a** European country
:::

**Lỗi 2: Bỏ sót mạo từ trước danh từ có tính từ bổ nghĩa**
:::example
- ❌ She is beautiful woman.
- ✅ She is **a** beautiful woman.
- ❌ It was interesting experience.
- ✅ It was **an** interesting experience.
:::

**Lỗi 3: Quên "the" với địa điểm công cộng xác định**
:::example
- ❌ She's at library.
- ✅ She's at **the** library.
- ❌ I'll meet you at airport.
- ✅ I'll meet you at **the** airport.
:::

**Lỗi 4: Dùng "the" với nhận xét chung (plural / uncountable)**
:::example
- ❌ I like the apples. *(nói chung về táo)*
- ✅ I like **apples**.
- ❌ The knowledge is power.
- ✅ **Knowledge** is power.
- ✅ **The** knowledge gained from this course is invaluable. *(kiến thức cụ thể)*
:::

---

## 5. Tóm Tắt Nhanh — Sơ Đồ Quyết Định

```
Danh từ đó là gì?
│
├─ Danh từ riêng (tên người, thành phố, quốc gia...)
│   ├─ Có thành phần chung (United, Republic...) → THE
│   └─ Không → KHÔNG có mạo từ
│
├─ Danh từ không đếm được / số nhiều mang nghĩa chung
│   → KHÔNG có mạo từ
│
└─ Danh từ đếm được số ít
    ├─ Cả hai đã biết / đã nhắc trước → THE
    └─ Chưa xác định / lần đầu nhắc → A / AN
```

:::tip
**Mẹo TOEIC:**
- Blank sau **my/his/their/this/that/these/those** → KHÔNG dùng mạo từ
- Blank trước danh từ số nhiều mang nghĩa chung → KHÔNG dùng mạo từ
- **Superlative** (nhất, most, -est) → luôn có **the** đứng trước
- **Ordinal numbers** (first, second, last) → luôn có **the**
- **Tên nhạc cụ** → luôn có **the** (play the piano)
:::
"""


async def update():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(GrammarTopic).where(GrammarTopic.slug == "articles")
        )
        topic = result.scalar_one_or_none()
        if not topic:
            print("ERROR: Articles topic not found")
            return
        topic.summary = ARTICLES_SUMMARY
        await db.commit()
        print(f"Updated Articles summary ({len(ARTICLES_SUMMARY)} chars)")


if __name__ == "__main__":
    asyncio.run(update())
