"""Update Conjunctions & Connectors summary with comprehensive content."""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.grammar_topic import GrammarTopic

SUMMARY = """## Liên Từ & Từ Nối (Conjunctions & Connectors)

> Liên từ và từ nối là các từ/cụm từ dùng để **kết nối ý tưởng, mệnh đề và câu** với nhau, thể hiện mối quan hệ logic giữa các phần trong bài viết hoặc bài nói.

---

## 1. Liên Từ Kết Hợp (Coordinating Conjunctions)

**Từ khóa ghi nhớ: FANBOYS** — For, And, Nor, But, Or, Yet, So

Nối hai **mệnh đề độc lập** (mỗi vế có thể đứng thành câu riêng).

| Liên từ | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| **and** | bổ sung, thêm vào | Sales grew, **and** profit margins improved. |
| **but** | tương phản trực tiếp | The plan was approved, **but** funding was limited. |
| **or** | lựa chọn / hậu quả nếu không | Submit today, **or** your application will be rejected. |
| **so** | kết quả, hậu quả | The deadline was tight, **so** we worked overtime. |
| **yet** | tương phản bất ngờ (= but, trang trọng hơn) | The task was difficult, **yet** the team completed it on time. |
| **for** | nguyên nhân (trang trọng, văn viết) | He resigned, **for** he was deeply unhappy with the direction. |
| **nor** | phủ định thêm (sau neither/not) | She didn't attend, **nor** did she send a representative. |

:::warning
**Quy tắc dấu phẩy:** Khi FANBOYS nối hai mệnh đề độc lập, đặt **dấu phẩy trước** liên từ.
- ✅ The report was late, **but** the quality was excellent.
- ❌ The report was late **but** the quality was excellent.

**Ngoại lệ:** Không cần dấu phẩy khi nối hai từ/cụm từ ngắn (không phải hai mệnh đề hoàn chỉnh):
- She is smart **and** hardworking. *(không có subject ở vế sau)*
:::

---

## 2. Liên Từ Phụ Thuộc (Subordinating Conjunctions)

Nối **mệnh đề phụ** vào mệnh đề chính. Mệnh đề phụ **không thể đứng riêng**.

:::tip
**Quy tắc dấu phẩy:**
- Mệnh đề phụ **đứng đầu câu** → **có dấu phẩy** sau nó.
- Mệnh đề phụ **đứng cuối câu** → **không cần dấu phẩy**.

✅ **Although** it was raining, we continued the outdoor event.
✅ We continued the outdoor event **although** it was raining.
:::

---

### 2.1 Thời Gian (Time)

| Liên từ | Ý nghĩa | Ghi chú |
|---------|---------|---------|
| **when** | khi | hành động xảy ra cùng lúc / ngay sau |
| **while / as** | trong khi | hai hành động cùng diễn ra song song |
| **before** | trước khi | |
| **after** | sau khi | |
| **until / till** | cho đến khi | hành động tiếp diễn đến một thời điểm |
| **as soon as / once** | ngay khi | nhấn mạnh tính tức thì |
| **since** | kể từ khi | dùng với thì hoàn thành |
| **whenever** | mỗi khi, bất cứ khi nào | |
| **by the time** | vào lúc mà, trước khi | thường kèm thì hoàn thành |
| **the moment (that) / the minute (that)** | ngay khi, ngay lúc | tương đương as soon as |

:::example
- **As soon as** the manager approves the budget, we will proceed.
- **By the time** the team arrived, the meeting had already ended.
- **The moment** she walked in, everyone stood up.
- We hadn't started **until** all stakeholders confirmed their attendance.
:::

**Cấu trúc đặc biệt — nâng cao:**

| Cấu trúc | Ý nghĩa | Ví dụ |
|----------|---------|-------|
| **No sooner...than** | vừa...đã ngay | No sooner **had** we launched the product **than** a competitor copied it. |
| **Hardly/Scarcely...when** | vừa mới...thì | Hardly **had** the meeting started **when** the power went out. |
| **Ever since** | kể từ khi (nhấn mạnh) | **Ever since** she joined, performance has improved steadily. |

:::warning
Sau **no sooner / hardly / scarcely** → đảo ngữ (inversion): had + S + V3

- No sooner **had the CEO arrived** than the press conference began. *(trang trọng)*
:::

---

### 2.2 Nguyên Nhân (Cause/Reason)

> because, since, as, for, now that, seeing that, given that, in that

| Liên từ | Độ trang trọng | Ý nghĩa & Ghi chú |
|---------|--------------|-------------------|
| **because** | thông thường | nguyên nhân trực tiếp, nhấn mạnh nhất |
| **since** | trung bình | nguyên nhân đã biết, thường đứng đầu câu |
| **as** | trung bình | nguyên nhân đã biết, đứng đầu câu, yếu hơn because |
| **for** | trang trọng | văn viết, đứng giữa câu sau dấu phẩy |
| **now that** | thông thường | vì bây giờ (nguyên nhân mới xảy ra) |
| **given that** | trang trọng | xét rằng, trong bối cảnh |
| **seeing that** | thông thường | vì thấy rằng |
| **in that** | trang trọng | ở chỗ là, theo nghĩa là |

:::example
- We cancelled the event **because** the venue was unavailable.
- **Since** everyone has agreed, let's move forward with the plan.
- **As** the budget was limited, we had to prioritize key activities.
- The proposal was rejected, **for** it lacked sufficient data.
- **Now that** the new system is live, training must begin immediately.
- The new policy is problematic **in that** it affects part-time workers disproportionately.
:::

:::warning
**Phân biệt SINCE:**
- **Since** (nguyên nhân) = as, because → không dùng với thì hoàn thành
- **Since** (thời gian) = từ khi → **dùng** với thì hoàn thành

✅ **Since** he is the most experienced, he should lead the team. *(nguyên nhân)*
✅ She has worked here **since** 2019. *(thời gian)*
:::

---

### 2.3 Mục Đích (Purpose)

| Cấu trúc | Ghi chú | Ví dụ |
|----------|---------|-------|
| **so that + can/could/will/would** | mục đích (thông thường) | We adjusted the schedule **so that** everyone could attend. |
| **in order that** | trang trọng hơn so that | Training was conducted **in order that** staff would meet standards. |
| **in order to / so as to + V** | ngắn gọn, không cần subject mới | She arrived early **in order to** prepare the presentation. |
| **for fear that** | sợ rằng, phòng khi | He double-checked everything **for fear that** mistakes would occur. |
| **lest** | e rằng (rất trang trọng, + should) | He rehearsed many times **lest** he should forget his lines. |

:::example
- We simplified the form **so that** applicants could complete it quickly.
- She took detailed notes **in order not to** miss any important points.
- Leave early **for fear that** you might miss the train.
:::

:::warning
**So that** (mục đích) ≠ **so...that** (kết quả):
- The system was designed **so that** users could navigate easily. *(mục đích — có thể)*
- The system was **so** complex **that** users couldn't navigate it. *(kết quả — xảy ra rồi)*
:::

---

### 2.4 Kết Quả (Result)

| Cấu trúc | Ví dụ |
|----------|-------|
| **so + adj/adv + that** | The report was **so detailed that** it took three hours to review. |
| **such + (a/an) + adj + noun + that** | It was **such an impressive** presentation **that** investors immediately committed. |
| **such that** (trang trọng) | The damage was **such that** the entire system needed replacing. |

---

### 2.5 Nhượng Bộ / Tương Phản (Concession/Contrast)

| Liên từ | Ý nghĩa | Ghi chú |
|---------|---------|---------|
| **although / though / even though** | mặc dù, dù | though thông thường nhất, even though nhấn mạnh |
| **while / whereas** | trong khi (tương phản) | nhấn mạnh sự đối lập giữa hai vế |
| **even if** | ngay cả khi (giả định) | không chắc xảy ra |
| **no matter how/what/when/where** | dù thế nào đi nữa | |
| **despite the fact that** | mặc dù thực tế là | = although nhưng trang trọng hơn |
| **however + adj/adv** | dù...đến đâu | However hard she tries, she can't seem to pass. |
| **whatever** | dù cái gì | Whatever happens, stay calm. |
| **whoever / whenever / wherever** | dù ai / lúc nào / ở đâu | |

:::example
- **Although** the market was challenging, we exceeded our targets.
- **Even though** costs rose significantly, we maintained profitability.
- **Even if** it rains, the outdoor event will proceed as planned. *(giả định)*
- **No matter how** hard we try, there will always be room for improvement.
- **While** the sales team exceeded targets, **whereas** the marketing team fell short. ❌
- Sales increased, **while** costs remained flat. ✅ *(while = contrast)*
- Sales increased in Region A, **whereas** they declined in Region B. ✅ *(stronger contrast)*
:::

---

### 2.6 Điều Kiện (Condition)

| Liên từ | Ý nghĩa |
|---------|---------|
| **if** | nếu |
| **unless** | nếu không, trừ khi (= if...not) |
| **provided (that) / providing (that)** | với điều kiện là |
| **as long as / so long as** | miễn là |
| **in case** | phòng khi (precaution) |
| **only if** | chỉ khi (nhấn mạnh điều kiện) |
| **on condition that** | với điều kiện là (trang trọng) |
| **suppose / supposing (that)** | giả sử như |
| **given that** | xét rằng, với điều kiện là |

---

### 2.7 Cách Thức (Manner)

| Liên từ | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| **as** | theo cách mà | Do **as** I say, not as I do. |
| **as if / as though** | như thể là (giả định) | She spoke **as if** she were the CEO already. |
| **the way (that)** | theo cách mà | Complete the form **the way** the instructions say. |
| **how** | cách thức | I'll show you **how** it's done. |

:::example
- He presented the data **as if** he had spent weeks preparing. *(as if + past — giả định)*
- Everything went **as** planned. *(theo đúng kế hoạch)*
- She managed the crisis **as though** nothing serious had happened.
:::

---

### 2.8 Nơi Chốn (Place)

| Liên từ | Ví dụ |
|---------|-------|
| **where** | Set up your workstation **where** you feel most productive. |
| **wherever** | **Wherever** you work, maintain professional standards. |

---

## 3. Liên Từ Tương Quan (Correlative Conjunctions)

Luôn đi theo **cặp**. Cấu trúc ngữ pháp sau mỗi vế phải **song song (parallel)**.

| Cặp | Ý nghĩa | Ví dụ |
|-----|---------|-------|
| **both...and** | cả...lẫn | **Both** the quality **and** the price are competitive. |
| **either...or** | hoặc...hoặc | We can **either** reduce costs **or** increase revenue. |
| **neither...nor** | không...cũng không | **Neither** the manager **nor** the team was informed. |
| **not only...but also** | không chỉ...mà còn | The update **not only** improves speed **but also** enhances security. |
| **not...but** | không phải...mà là | The issue is **not** the budget **but** the timeline. |
| **whether...or** | dù...hay | **Whether** you agree **or** not, the policy stands. |
| **as...as** | cũng...như | She is **as** qualified **as** any other candidate. |
| **the more...the more** | càng...càng | **The more** you practice, **the better** you become. |
| **scarcely/hardly...when** | vừa...thì | **Scarcely** had we started **when** problems arose. |
| **no sooner...than** | vừa...đã | **No sooner** had he spoken **than** the phone rang. |

### Quy tắc Parallel Structure (Song Song)

Các thành phần sau mỗi vế của cặp liên từ phải là **cùng loại từ/cụm từ**:

:::example
✅ The new system is **both** reliable **and** efficient. *(adj + adj)*
❌ The new system is **both** reliable **and** it saves energy. *(adj + clause)*

✅ We need someone who can **not only** design **but also** code. *(V + V)*
❌ We need someone who can **not only** design **but also** coding. *(V + V-ing)*

✅ **Either** call us **or** send an email. *(V + V)*
❌ **Either** you can call **or** email. *(clause + V)*
:::

---

## 4. Trạng Từ Liên Kết (Conjunctive Adverbs / Transition Words)

Đứng **đầu câu** sau dấu **; (chấm phẩy)** hoặc **. (chấm)**. Luôn có **dấu phẩy** sau.

Có thể đứng giữa câu (giữa hai dấu phẩy) nhưng ít phổ biến hơn.

### 4.1 Tương Phản & Nhượng Bộ

| Từ nối | Ý nghĩa | Mức độ trang trọng |
|--------|---------|-------------------|
| **however** | tuy nhiên | trung bình |
| **nevertheless** | dù vậy (nhấn mạnh hơn however) | trang trọng |
| **nonetheless** | dù vậy (= nevertheless) | trang trọng |
| **on the other hand** | mặt khác | trung bình |
| **in contrast** | ngược lại | trang trọng |
| **on the contrary** | trái lại (phủ nhận điều vừa nói) | trang trọng |
| **that said / having said that** | tuy nhiên, dù vậy | thông thường |
| **still** | vậy mà, nhưng vẫn | thông thường |
| **yet** | thế nhưng | thông thường |

:::example
- The budget was reduced; **however**, the quality of output remained high.
- The project faced many obstacles; **nevertheless**, the team delivered on time.
- Our costs are higher. **On the other hand**, our quality is unmatched.
- He lacked experience. **That said**, his potential was undeniable.
:::

### 4.2 Nguyên Nhân & Kết Quả

| Từ nối | Ý nghĩa |
|--------|---------|
| **therefore** | do đó, vì vậy |
| **thus** | vì vậy, do đó (trang trọng hơn) |
| **hence** | do đó, vì thế (trang trọng) |
| **consequently** | kết quả là |
| **as a result** | kết quả là |
| **as a consequence** | như một hệ quả |
| **for this reason** | vì lý do này |
| **accordingly** | do đó, phù hợp với đó |

:::example
- Sales declined significantly; **therefore**, we need to revise our strategy.
- The system was outdated; **consequently**, performance suffered.
- Costs have risen; **as a result**, we must adjust our pricing.
- The client requested changes; **accordingly**, we updated the proposal.
:::

### 4.3 Bổ Sung & Thêm Ý

| Từ nối | Ý nghĩa |
|--------|---------|
| **moreover** | hơn nữa (thêm ý quan trọng hơn) |
| **furthermore** | hơn nữa (= moreover, trang trọng) |
| **in addition** | thêm vào đó |
| **additionally** | ngoài ra |
| **besides** | ngoài ra, hơn nữa |
| **what is more** | hơn thế nữa |
| **on top of that** | thêm vào đó (thông thường) |
| **also** | cũng, ngoài ra |

### 4.4 Trình Tự & Thứ Tự

| Từ nối | Ý nghĩa |
|--------|---------|
| **first / firstly** | thứ nhất, trước tiên |
| **second / secondly** | thứ hai |
| **then / next** | sau đó, tiếp theo |
| **subsequently** | tiếp theo sau đó |
| **finally / lastly** | cuối cùng |
| **to begin with** | để bắt đầu |
| **to start with** | để bắt đầu |
| **last but not least** | cuối cùng nhưng không kém phần quan trọng |

### 4.5 Nhấn Mạnh (Emphasis)

| Từ nối | Ý nghĩa |
|--------|---------|
| **in particular / particularly** | đặc biệt là |
| **especially** | đặc biệt |
| **above all** | quan trọng hơn cả, nhất là |
| **notably** | đáng chú ý là |
| **indeed** | thực vậy, thật ra |
| **in fact / as a matter of fact** | thực ra, thực tế là |
| **certainly / undoubtedly** | chắc chắn là |

### 4.6 Ví Dụ & Minh Họa

| Từ nối | Ý nghĩa |
|--------|---------|
| **for example / for instance** | ví dụ |
| **such as** | chẳng hạn như |
| **to illustrate** | để minh họa |
| **namely** | cụ thể là, tức là |
| **in particular** | cụ thể là |

### 4.7 Làm Rõ & Diễn Giải

| Từ nối | Ý nghĩa |
|--------|---------|
| **that is (to say) / i.e.** | tức là, nghĩa là |
| **in other words** | nói cách khác |
| **to put it differently** | nói theo cách khác |
| **to clarify** | để làm rõ |

### 4.8 Tương Đồng

| Từ nối | Ý nghĩa |
|--------|---------|
| **similarly** | tương tự |
| **likewise** | tương tự như vậy |
| **in the same way** | theo cách tương tự |
| **by the same token** | cũng vì lý do đó |

### 4.9 Thay Thế & Điều Kiện Ngược

| Từ nối | Ý nghĩa |
|--------|---------|
| **otherwise** | nếu không |
| **alternatively** | hoặc thay vào đó |
| **instead** | thay vào đó |

### 4.10 Kết Luận & Tóm Tắt

| Từ nối | Ý nghĩa |
|--------|---------|
| **in conclusion / to conclude** | tóm lại, kết luận |
| **to sum up / in summary** | tóm tắt lại |
| **in brief / in short** | tóm lại ngắn gọn |
| **overall** | nhìn chung |
| **to recap** | tóm tắt lại |
| **all in all** | nói chung |

---

## 5. Giới Từ vs Liên Từ (So Sánh Chi Tiết)

| Ý nghĩa | Liên từ → + Mệnh đề (S+V) | Giới từ → + Danh từ / V-ing |
|---------|--------------------------|------------------------------|
| Mặc dù | although / though / even though | despite / in spite of |
| Vì | because / since / as / for | because of / due to / owing to / on account of |
| Trong khi | while / when | during |
| Trước khi | before | before + V-ing / prior to |
| Ngay khi | as soon as | upon + V-ing |
| Ngoại trừ | except that | except / apart from |
| Theo | as | according to |

:::example
- **Although** demand fell, we maintained our market share. *(liên từ + mệnh đề)*
- **Despite** falling demand, we maintained our market share. *(giới từ + V-ing)*
- **Despite the fact that** demand fell, we maintained our market share. *(despite the fact that + mệnh đề)*

- **Because** costs rose, we revised the budget. *(liên từ + mệnh đề)*
- **Because of** rising costs, we revised the budget. *(giới từ + cụm danh từ)*
- **Due to** a rise in costs, we revised the budget. *(giới từ + cụm danh từ)*
- **Owing to** cost increases, we revised the budget. *(giới từ + cụm danh từ)*

- **While** the CEO was traveling, the VP handled operations. *(liên từ + mệnh đề)*
- **During** the CEO's travel, the VP handled operations. *(giới từ + danh từ)*

- She resigned **upon** receiving the offer from a rival firm. *(upon + V-ing = ngay khi)*
:::

---

## 6. Phân Biệt Các Cặp Dễ Nhầm

### WHILE vs ALTHOUGH vs WHEREAS

| Từ | Ý nghĩa chính | Dùng khi |
|----|--------------|---------|
| **while** | trong khi (thời gian) | hai hành động song song |
| **while** | mặc dù (nhượng bộ nhẹ) | tương phản, vế sau quan trọng hơn |
| **although** | mặc dù (nhượng bộ) | nhấn mạnh sự ngạc nhiên/tương phản |
| **whereas** | trong khi đó (tương phản mạnh) | so sánh hai thực tế trái ngược |

:::example
- **While** I was preparing the slides, she was rehearsing. *(thời gian — song song)*
- **While** I understand your concern, I still think we should proceed. *(nhượng bộ nhẹ)*
- **Although** he had little experience, he was the best candidate. *(nhượng bộ — ngạc nhiên)*
- Sales rose in Q1, **whereas** they fell sharply in Q2. *(tương phản mạnh — đối lập hai thực tế)*
:::

### BECAUSE vs SINCE vs AS vs FOR

| Từ | Vị trí | Độ nhấn mạnh | Ghi chú |
|----|--------|-------------|---------|
| **because** | giữa hoặc đầu câu | mạnh nhất | nguyên nhân trực tiếp, quan trọng |
| **since** | thường đầu câu | trung bình | nguyên nhân đã biết, ít nhấn |
| **as** | thường đầu câu | yếu nhất | nguyên nhân đã rõ ràng |
| **for** | giữa câu | trang trọng | văn viết, sau dấu phẩy |

:::example
- We cancelled the flight **because** there was a severe storm. *(nguyên nhân chính)*
- **Since** everyone is here, let's begin the meeting. *(nguyên nhân đã biết)*
- **As** she was the most senior, she chaired the session. *(nguyên nhân hiển nhiên)*
- He could not proceed, **for** the documents had not been signed. *(trang trọng)*
:::

### SO vs THEREFORE vs THUS vs CONSEQUENTLY vs HENCE

| Từ | Loại | Vị trí | Độ trang trọng |
|----|------|--------|---------------|
| **so** | Liên từ (FANBOYS) | giữa câu | thông thường |
| **therefore** | Trạng từ liên kết | đầu câu / giữa câu | trung bình |
| **thus** | Trạng từ liên kết | đầu câu / giữa câu | trang trọng |
| **consequently** | Trạng từ liên kết | đầu câu | trang trọng |
| **hence** | Trạng từ liên kết | đầu câu / giữa câu | rất trang trọng |

:::example
- Costs increased, **so** we raised our prices. *(liên từ — thông thường)*
- Costs increased; **therefore**, we had to raise our prices. *(trạng từ — trung bình)*
- The data was incomplete; **thus**, the analysis could not be finalized. *(trang trọng)*
- The supplier failed to deliver; **consequently**, production was halted. *(trang trọng)*
:::

### BUT vs HOWEVER vs NEVERTHELESS vs NONETHELESS vs YET

| Từ | Loại | Vị trí | Mức độ tương phản |
|----|------|--------|-----------------|
| **but** | Liên từ | giữa câu | trực tiếp, thông thường |
| **however** | Trạng từ | đầu/giữa câu | rõ ràng, phổ biến |
| **nevertheless** | Trạng từ | đầu câu | mạnh, nhấn mạnh "dù vậy vẫn" |
| **nonetheless** | Trạng từ | đầu câu | = nevertheless |
| **yet** | Liên từ/Trạng từ | giữa câu | bất ngờ, nhẹ hơn but |
| **still** | Trạng từ | giữa câu | vẫn còn, dù vậy |

:::example
- The task was hard, **but** we finished it. *(thông thường)*
- The task was hard; **however**, we finished it. *(rõ hơn, văn bản)*
- The team faced enormous pressure; **nevertheless**, they delivered excellent results. *(nhấn mạnh)*
- The results were disappointing; **nonetheless**, we learned valuable lessons. *(tương tự)*
:::

---

## 7. Mức Độ Trang Trọng (Formality Register)

| Informal (nói/email thông thường) | Neutral | Formal (báo cáo/học thuật) |
|----------------------------------|---------|--------------------------|
| but | however | nevertheless / nonetheless |
| so | therefore | consequently / hence / thus |
| also | in addition | furthermore / moreover |
| like | such as | for instance / namely |
| because | as / since | owing to / given that |
| anyway | regardless | notwithstanding |

---

## 8. Dấu Câu Với Liên Từ & Từ Nối

| Trường hợp | Quy tắc | Ví dụ |
|-----------|---------|-------|
| **FANBOYS nối 2 mệnh đề** | Dấu phẩy **trước** FANBOYS | Sales rose, **but** profits fell. |
| **Mệnh đề phụ đầu câu** | Dấu phẩy **sau** mệnh đề phụ | **Although** it was late, we continued. |
| **Mệnh đề phụ cuối câu** | Không cần dấu phẩy | We continued **although** it was late. |
| **Conjunctive adverb** | Dấu **;** trước + dấu **,** sau | Sales rose; **however**, profits fell. |
| **Conjunctive adverb giữa câu** | Hai dấu phẩy bao quanh | Sales, **however**, increased slightly. |

---

:::tip
**Mẹo làm bài TOEIC:**
- Blank giữa hai mệnh đề hoàn chỉnh (S+V...___S+V) → **liên từ** (although, because, while) hoặc **trạng từ** sau dấu chấm phẩy (however, therefore)
- Blank trước **danh từ / V-ing** → **giới từ** (despite, because of, during)
- Thấy dấu **;** → chọn **trạng từ liên kết** (however, therefore, moreover...)
- Thấy hai vế **đối lập** → although / even though / however / nevertheless / despite
- Thấy hai vế **nguyên nhân–kết quả** → because / since / therefore / consequently / as a result
- **Parallel structure**: both/either/neither/not only → phần tử tiếp theo phải cùng **cấu trúc ngữ pháp**
- Phân biệt **so that** (mục đích) với **so...that** (kết quả) qua ngữ nghĩa câu
:::
"""


async def update():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(GrammarTopic).where(GrammarTopic.slug == "conjunctions-connectors")
        )
        topic = result.scalar_one_or_none()
        if not topic:
            print("ERROR: Topic not found")
            return
        topic.summary = SUMMARY
        await db.commit()
        print(f"Updated Conjunctions & Connectors ({len(SUMMARY):,} chars)")


if __name__ == "__main__":
    asyncio.run(update())
