"""
One-time script: update the Gerunds & Infinitives topic with comprehensive content.
"""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.grammar_topic import GrammarTopic

GERUNDS_INFINITIVES_SUMMARY = """## Danh Động Từ & Động Từ Nguyên Mẫu (Gerunds & Infinitives)

> **Gerund (V-ing)** và **Infinitive (to + V)** đều có thể đóng vai trò như danh từ trong câu. Việc chọn đúng dạng là một trong những điểm ngữ pháp quan trọng nhất trong TOEIC.

---

## 1. Danh Động Từ (Gerund = V-ing)

### Chức năng của Gerund

| Vai trò | Ví dụ |
|---------|-------|
| **Làm chủ ngữ** | **Managing** a team requires strong communication skills. |
| **Làm tân ngữ** | She enjoys **networking** at industry events. |
| **Sau giới từ** | He is responsible **for overseeing** the project. |
| **Làm bổ ngữ** | Her main hobby is **reading** financial reports. |
| **Sau "it's worth"** | This investment is worth **considering**. |

:::warning
**Quy tắc vàng:** Sau **mọi giới từ** (in, on, at, for, about, of, with, without, after, before, by, despite, instead of...) → luôn dùng **V-ing**.
:::

### Danh sách động từ theo sau là Gerund

:::tip
**Nhóm 1 — Thích/Ghét/Tránh:**
enjoy, like, love, hate, dislike, prefer, don't mind, can't stand, can't help, appreciate, resent, resist, miss

**Nhóm 2 — Dừng/Hoàn thành:**
finish, stop, quit, give up, complete, avoid, delay, postpone, put off

**Nhóm 3 — Gợi ý/Thừa nhận:**
suggest, recommend, consider, admit, deny, risk, imagine, involve, justify

**Nhóm 4 — Tiếp tục:**
keep, keep on, go on, continue *(cả hai)*

**Nhóm 5 — Cụm động từ giới từ:**
look forward to, be used to, get used to, object to, be accustomed to, be committed to, be dedicated to, be opposed to, contribute to, resort to, confess to, admit to
:::

:::example
- The board **suggested implementing** a new policy.
- She **avoids making** decisions without data.
- I **look forward to meeting** you next week. *(to là giới từ)*
- He **finished reviewing** the contracts.
- We **considered hiring** an external consultant.
- She **admitted taking** the wrong file.
- They **postponed launching** the product until Q3.
- He **resisted accepting** the unfavorable terms.
:::

### Cụm giới từ thường gặp + Gerund

| Cụm | Ví dụ |
|-----|-------|
| be good/bad **at** | She is good **at negotiating** contracts. |
| be interested **in** | He is interested **in expanding** to new markets. |
| be responsible **for** | She is responsible **for managing** the budget. |
| be capable **of** | The system is capable **of processing** 1,000 requests/sec. |
| be afraid **of** | He is afraid **of making** mistakes. |
| be excited **about** | They are excited **about launching** the app. |
| be tired **of** | She is tired **of dealing** with complaints. |
| be famous **for** | The company is famous **for producing** quality goods. |
| be used **to** | I am used **to working** under pressure. |
| thank you **for** | Thank you **for attending** today's seminar. |
| instead **of** | He sent an email instead **of calling** directly. |
| by + V-ing | She improved her skills **by practicing** daily. |
| without + V-ing | He left **without saying** goodbye. |
| despite/in spite of | **Despite working** hard, he missed the deadline. |
| after/before + V-ing | **After reviewing** the data, she wrote the report. |

---

## 2. Động Từ Nguyên Mẫu (Infinitive = To + V)

### Chức năng của Infinitive

| Vai trò | Ví dụ |
|---------|-------|
| **Làm chủ ngữ** | **To succeed** in business requires perseverance. |
| **Diễn tả mục đích** | She traveled **to attend** the conference. |
| **Sau tính từ** | We are pleased **to announce** the results. |
| **Sau "it is + adj"** | It is important **to verify** all data. |
| **Sau danh từ** | She has the ability **to lead** a team effectively. |
| **Bổ ngữ chủ ngữ** | Our goal is **to achieve** 20% growth. |

### Danh sách động từ theo sau là Infinitive

:::tip
**Nhóm 1 — Muốn/Hy vọng/Quyết định:**
want, wish, hope, plan, decide, choose, intend, aim, determine, resolve

**Nhóm 2 — Đồng ý/Từ chối:**
agree, refuse, offer, promise, threaten, volunteer, consent, decline

**Nhóm 3 — Cố gắng/Thất bại:**
attempt, try *(cố gắng)*, manage, fail, struggle, endeavor

**Nhóm 4 — Trông có vẻ:**
seem, appear, tend, prove, happen, claim, pretend

**Nhóm 5 — Có đủ tiền/Cần thiết:**
afford, need, deserve, demand, expect, require

**Nhóm 6 — Yêu cầu người khác:**
ask, tell, advise, allow, encourage, force, invite, order, permit, persuade, remind, warn, urge
:::

:::example
- The company **decided to restructure** its operations.
- She **managed to complete** the report before the deadline.
- Management **agreed to review** the compensation package.
- We **expect to launch** the product next quarter.
- He **failed to meet** the sales target.
- She **offered to help** with the presentation.
- They **refused to sign** the contract without modifications.
- The manager **encouraged** the team **to innovate**.
- HR **reminded** all staff **to complete** the training.
:::

### Động từ + Tân ngữ + Infinitive

Cấu trúc: **Verb + Object + to-infinitive**

| Nhóm | Động từ | Ví dụ |
|------|---------|-------|
| **Yêu cầu** | tell, ask, order, command | She **told** him **to submit** the report. |
| **Cho phép** | allow, permit, enable, authorize | They **allowed** us **to work** from home. |
| **Khuyên/Cảnh báo** | advise, warn, remind, urge | He **warned** them **not to exceed** the budget. |
| **Khuyến khích** | encourage, motivate, inspire | She **encouraged** him **to apply** for the role. |
| **Ép buộc** | force, require, compel, cause | The law **requires** companies **to disclose** data. |
| **Mong đợi** | expect, want, need | We **need** you **to finalize** the report today. |
| **Mời** | invite, hire | They **invited** her **to speak** at the event. |

:::warning
**Lưu ý:** Các động từ **advise, allow, permit, require, urge, force** có thể dùng cả hai cấu trúc:
- **advise + V-ing** (không có tân ngữ): The doctor **advises eating** less salt.
- **advise + obj + to-inf** (có tân ngữ): The doctor **advised him to eat** less salt.
:::

---

## 3. Động Từ Dùng Cả Hai — Nghĩa THAY ĐỔI

Đây là điểm thi quan trọng nhất trong chủ đề này!

| Động từ | + Gerund (V-ing) | + Infinitive (to + V) |
|---------|-----------------|----------------------|
| **remember** | nhớ lại việc đã làm (quá khứ) | nhớ phải làm (tương lai) |
| **forget** | quên mất việc đã làm | quên không làm |
| **regret** | hối tiếc về việc đã làm | tiếc phải thông báo |
| **stop** | dừng hẳn việc đang làm | dừng lại để làm gì khác |
| **try** | thử xem kết quả thế nào | cố gắng đạt được điều gì |
| **mean** | có nghĩa là / kéo theo | có ý định / dự định |
| **go on** | tiếp tục việc đang làm | chuyển sang việc khác |
| **need** | cần được làm (= bị động) | cần làm (chủ động) |

:::example
**remember:**
- I remember **meeting** her at the conference. *(nhớ lại đã gặp — quá khứ)*
- Remember **to submit** the form before Friday. *(nhớ phải nộp — tương lai)*

**stop:**
- He stopped **smoking**. *(bỏ thuốc hẳn)*
- He stopped **to check** his phone. *(dừng lại để kiểm tra — mục đích)*

**try:**
- She **tried taking** a cold shower to stay awake. *(thử xem có tỉnh không)*
- She **tried to finish** the report but couldn't. *(cố gắng nhưng không xong)*

**regret:**
- We regret **to inform** you that your application was unsuccessful. *(tiếc phải thông báo)*
- She regrets **not taking** the opportunity when she had the chance. *(hối tiếc đã không làm)*

**need:**
- The report **needs updating**. *(= needs to be updated — cần được cập nhật)*
- She **needs to update** the report. *(cô ấy cần tự làm)*

**mean:**
- Missing the flight **means losing** the whole day. *(có nghĩa là mất cả ngày)*
- I **meant to call** you yesterday but forgot. *(có ý định gọi)*

**go on:**
- He **went on talking** for another hour. *(tiếp tục nói — cùng chủ đề)*
- After the break, she **went on to discuss** the budget. *(chuyển sang nội dung khác)*
:::

---

## 4. Động Từ Dùng Cả Hai — Nghĩa KHÔNG ĐỔI

> begin, start, continue, like, love, hate, prefer *(khi không có trạng thái tiến hành)*

:::example
- She **likes to work / working** independently. *(nghĩa như nhau)*
- It **began to rain / raining** heavily.
- He **continued to work / working** after midnight.
:::

:::warning
**Ngoại lệ:** Khi động từ chính ở dạng tiến hành (-ing), không dùng gerund theo sau:
- ❌ She **is liking working** from home.
- ✅ She **likes working** from home.
:::

---

## 5. Động Từ Nguyên Mẫu Không "To" (Bare Infinitive)

### Sau động từ khuyết thiếu (Modal Verbs)

:::example
- You **should review** the contract carefully.
- She **can handle** the presentation.
- We **must submit** the application by Monday.
:::

### Sau make / let / have (causative)

| Cấu trúc | Nghĩa | Ví dụ |
|---------|-------|-------|
| **make** + obj + V | ép buộc | The boss **made** him **redo** the report. |
| **let** + obj + V | cho phép | Please **let** me **know** your decision. |
| **have** + obj + V | nhờ/bảo | She **had** her assistant **book** the flights. |
| **help** + obj + V/to V | giúp | This tool **helps** employees **track** progress. |

:::warning
**So sánh have vs get:**
- **have** + obj + **bare V** → nhờ làm (chủ động): She **had** IT **fix** the computer.
- **get** + obj + **to-inf** → nhờ/thuyết phục: She **got** IT **to fix** the computer.
- **have/get** + obj + **V3** → nhờ được làm (thụ động): She **had** the computer **fixed**.
:::

### Sau động từ tri giác (Perception Verbs)

Cấu trúc: **see/hear/feel/watch/notice/observe + obj + V-ing** *(đang xảy ra)* hoặc **+ bare V** *(toàn bộ hành động)*

:::example
- I **saw** him **signing** the contract. *(đang ký — chứng kiến một phần)*
- I **saw** him **sign** the contract. *(ký xong — chứng kiến toàn bộ)*
- She **heard** someone **knocking** at the door.
- We **watched** the team **present** their findings.
- He **felt** his heart **beating** fast.
:::

---

## 6. Gerund & Infinitive Dạng Phủ Định

:::example
**Phủ định Gerund:** not + V-ing
- She **regrets not taking** the job offer.
- **Not knowing** the answer, he remained silent.
- He was criticized **for not submitting** the report on time.

**Phủ định Infinitive:** not + to + V
- Remember **not to leave** confidential files unattended.
- He decided **not to attend** the meeting.
- She chose **not to respond** to the email.
:::

---

## 7. Dạng Hoàn Thành (Perfect Form)

### Perfect Gerund: having + V3

Diễn tả hành động xảy ra **trước** hành động khác.

:::example
- **Having finished** the report, she sent it to the manager. *(hoàn thành trước khi gửi)*
- She denied **having taken** the money.
- He was proud of **having led** the project to success.
- **Not having received** a reply, we sent a follow-up email.
:::

### Perfect Infinitive: to have + V3

:::example
- She **seems to have forgotten** about the meeting. *(có vẻ đã quên)*
- He **is believed to have resigned**. *(được cho là đã từ chức)*
- They **claimed to have completed** the audit. *(tuyên bố đã hoàn thành)*
- I would like **to have attended** the conference. *(muốn tham dự nhưng không được)*
:::

---

## 8. Dạng Bị Động (Passive Form)

### Passive Gerund: being + V3

:::example
- She doesn't like **being interrupted** during meetings.
- He avoided **being seen** with the rival company.
- The CEO enjoyed **being welcomed** by the staff.
- The report needs **being revised** before submission. *(= needs to be revised)*
:::

### Passive Infinitive: to be + V3

:::example
- The contract needs **to be signed** by both parties.
- She expects **to be promoted** next quarter.
- The data is **to be submitted** by Friday.
- He wants **to be informed** of any changes.
:::

---

## 9. Gerund làm Chủ Ngữ — Sở Hữu Cách

Khi gerund làm chủ ngữ với người/vật cụ thể → dùng **tính từ sở hữu** hoặc **sở hữu cách (possessive)**

:::example
- **His leaving** early surprised everyone. *(sở hữu cách — trang trọng)*
- **The company's expanding** into Asia was a bold move.
- I appreciate **your helping** me with the report. *(= your help)*
- We understand **their refusing** to negotiate. *(= their refusal)*
:::

:::warning
Trong văn nói/không trang trọng, thường dùng tân ngữ thay vì sở hữu cách:
- I appreciate **you helping** me. *(ít trang trọng hơn)*
- We understand **them refusing**. *(thông dụng hơn trong văn nói)*
:::

---

## 10. Cấu Trúc Đặc Biệt Với Infinitive

### Infinitive Diễn Tả Mục Đích

| Cấu trúc | Ví dụ |
|---------|-------|
| **to + V** | She came **to discuss** the budget. |
| **in order to + V** | He stayed late **in order to finish** the report. |
| **so as to + V** | She spoke quietly **so as not to disturb** others. |
| **in order not to + V** | We left early **in order not to miss** the train. |

### Too + Adj/Adv + To-Infinitive

:::example
- The task is **too complex to complete** in one day. *(quá phức tạp đến mức không hoàn thành được)*
- She spoke **too quickly for us to understand**.
- He is **too young to be** a manager.
- The report is **too long to read** in an hour.
:::

### Adj/Adv + Enough + To-Infinitive

:::example
- She is **experienced enough to handle** the project.
- The system is **fast enough to process** real-time data.
- Is he **qualified enough to lead** the team?
- The budget isn't **large enough to cover** all expenses.
:::

### It + adj + (for sb) + To-Infinitive

:::example
- It is **important to verify** all information.
- It is **essential for all staff to complete** the training.
- It was **difficult to reach** an agreement.
- It is **unusual for him to arrive** late.
- It's **thoughtful of you to offer** to help. *(of + người = đánh giá phẩm chất)*
:::

:::tip
**Phân biệt "of" và "for":**
- **It is + adj tính cách người + of + sb + to do**: It's kind **of you** to help. *(kind, generous, stupid, rude, clever → mô tả người)*
- **It is + adj + for + sb + to do**: It is important **for you** to attend. *(important, difficult, easy, necessary → không mô tả người)*
:::

---

## 11. Danh Từ + Infinitive

Một số danh từ thường đi kèm với to-infinitive:

| Danh từ | Ví dụ |
|---------|-------|
| **ability** | She has the **ability to lead** effectively. |
| **decision** | His **decision to resign** shocked everyone. |
| **tendency** | There is a **tendency to underestimate** risks. |
| **effort** | Every **effort to reduce** costs was made. |
| **attempt** | Their **attempt to merge** failed. |
| **opportunity** | I had the **opportunity to attend** the summit. |
| **failure** | His **failure to respond** caused delays. |
| **permission** | She gave him **permission to leave** early. |
| **willingness** | Her **willingness to travel** is an asset. |
| **refusal** | His **refusal to compromise** ended the talks. |

---

## 12. Cụm Cố Định Quan Trọng

### Cụm dùng V-ing

| Cụm | Nghĩa | Ví dụ |
|-----|-------|-------|
| **It's worth + V-ing** | Đáng để làm | It's **worth investing** in training. |
| **It's no use/good + V-ing** | Vô ích khi làm | It's **no use complaining** about the policy. |
| **There's no point in + V-ing** | Không có ý nghĩa gì | There's **no point in delaying** the decision. |
| **have difficulty/trouble + V-ing** | gặp khó khăn khi | He **had difficulty writing** the report. |
| **spend time/money + V-ing** | dành thời gian/tiền làm | She **spent hours researching** the topic. |
| **waste time/money + V-ing** | lãng phí | Don't **waste time arguing**. |
| **be busy + V-ing** | đang bận làm | She is **busy preparing** for the presentation. |
| **go + V-ing** | đi làm hoạt động | Let's **go shopping** after work. |
| **can't help + V-ing** | không thể nhịn được | I **can't help laughing** at his jokes. |
| **be/get used to + V-ing** | quen với | He is **used to working** under pressure. |
| **be accustomed to + V-ing** | quen với | She is **accustomed to managing** large teams. |

### Cụm dùng Infinitive

| Cụm | Nghĩa | Ví dụ |
|-----|-------|-------|
| **be about to + V** | sắp làm | We **are about to sign** the contract. |
| **be supposed to + V** | được cho là phải | You **are supposed to submit** by Friday. |
| **be likely to + V** | có khả năng | Sales **are likely to increase** next quarter. |
| **be willing to + V** | sẵn sàng | She **is willing to work** overtime. |
| **be able to + V** | có thể | He **is able to handle** the pressure. |
| **be eager to + V** | háo hức muốn | They **are eager to start** the project. |
| **be reluctant to + V** | do dự, không muốn | He **is reluctant to delegate** tasks. |
| **be determined to + V** | quyết tâm | She **is determined to succeed**. |

---

## 13. Prefer: So Sánh Ưu Tiên

| Cấu trúc | Ví dụ |
|---------|-------|
| **prefer + V-ing + to + V-ing** | She **prefers working** from home **to commuting**. |
| **prefer + to-inf + rather than + bare V** | He **prefers to email rather than call**. |
| **would prefer + to-inf** | I **would prefer to reschedule** the meeting. |
| **would rather + bare V + than + bare V** | She **would rather stay than leave** early. |

---

## 14. Các Lỗi Thường Gặp

**Lỗi 1: Dùng gerund sau "to" của to-infinitive**
:::example
- ❌ She wants **to finishing** the report.
- ✅ She wants **to finish** the report.
:::

**Lỗi 2: Nhầm "to" giới từ và "to" của infinitive**
:::example
- ❌ She is **used to work** late. *(to = giới từ, sau đó phải là V-ing)*
- ✅ She is **used to working** late.
- ❌ She **used to working** late every day. *(used to + V = thói quen quá khứ)*
- ✅ She **used to work** late every day.
:::

**Lỗi 3: Quên "-ing" sau giới từ**
:::example
- ❌ He succeeded **in complete** the project.
- ✅ He succeeded **in completing** the project.
- ❌ She is good **at manage** people.
- ✅ She is good **at managing** people.
:::

**Lỗi 4: Dùng make/let với to-infinitive**
:::example
- ❌ The manager **made** him **to redo** the work.
- ✅ The manager **made** him **redo** the work. *(bare infinitive)*
- ❌ Please **let** me **to explain**.
- ✅ Please **let** me **explain**.
:::

**Lỗi 5: Nhầm need doing vs need to do**
:::example
- The car **needs checking**. *(= needs to be checked — cần được kiểm tra)*
- He **needs to check** the car. *(anh ấy cần tự kiểm tra)*
:::

---

## 15. Tóm Tắt Nhanh — Sơ Đồ Quyết Định

```
Sau GIỚI TỪ? → V-ING (luôn luôn)

Sau ĐỘNG TỪ KHUYẾT THIẾU? → BARE INFINITIVE

Sau MAKE / LET? → BARE INFINITIVE

Sau ĐỘNG TỪ TRI GIÁC (see/hear/watch...)?
  → V-ING (đang xảy ra) hoặc BARE INFINITIVE (toàn bộ)

Sau ĐỘNG TỪ CHÍNH?
  → Tra danh sách: chỉ Gerund / chỉ Infinitive / cả hai
  → Nếu nghĩa thay đổi: remember/forget/stop/try/regret/mean/need

Diễn tả MỤC ĐÍCH? → TO-INFINITIVE (in order to / so as to)

TOO + adj + ? → TO-INFINITIVE

Adj + ENOUGH + ? → TO-INFINITIVE
```

:::tip
**Mẹo làm bài TOEIC:**
- Sau **giới từ** → luôn **V-ing**
- **look forward to / be used to / get used to / object to / be accustomed to** → **V-ing** (to là giới từ)
- **make / let** → **bare V** | **allow / permit / require / ask / tell / want** → **to + V**
- **remember/forget** + V-ing = quá khứ | + to-inf = tương lai
- **stop** + V-ing = dừng hẳn | + to-inf = dừng lại để làm gì khác
- **try** + V-ing = thử xem | + to-inf = cố gắng
- **need** + V-ing = bị động | + to-inf = chủ động cần làm
- **having + V3** = perfect gerund (đã làm trước đó)
- **to have + V3** = perfect infinitive (đã làm trước đó)
:::
"""


async def update():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(GrammarTopic).where(GrammarTopic.slug == "gerunds-infinitives")
        )
        topic = result.scalar_one_or_none()
        if not topic:
            print("ERROR: Gerunds & Infinitives topic not found")
            return
        topic.summary = GERUNDS_INFINITIVES_SUMMARY
        await db.commit()
        print(f"Updated Gerunds & Infinitives summary ({len(GERUNDS_INFINITIVES_SUMMARY)} chars)")


if __name__ == "__main__":
    asyncio.run(update())
