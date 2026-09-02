---
knowledge_id: shared-clinic-profile
title: ملف العيادة
version: "0.1.0"
status: DRAFT
owner: clinic-owner
domain: marketing
source: ⟨لم تُملأ بعد — يملؤها الطبيب/ة أو من ينوب عنه/ها⟩
source_type: draft
created: "2026-08-21"
last_verified: null
next_review: null
used_by: []
sensitivity: LOW
patient_data_allowed: false
supersedes: null
tags: [clinic, profile, identity]
---

# ملف العيادة

> **DRAFT — لا يُستخدَم من أي مساعد حتى يُعتمَد.** كل حقل بلا قيمة مؤكَّدة يبقى فارغاً — لا تخمين ولا اختراع.

| الحقل | القيمة |
|---|---|
| اسم العيادة | ⟨املئيه⟩ |
| العنوان | ⟨املئيه⟩ |
| ساعات العمل | ⟨املئيها⟩ |
| رقم الحجز | ⟨املئيه⟩ |
| رقم الطوارئ | ⟨املئيه — يُستخدَم حرفياً في نص إحالة الطوارئ في clinical-firewall.md⟩ |
| طرق الدفع المقبولة | ⟨املئيها⟩ |
| قنوات التواصل | ⟨البقية من house-rules.md §١ بعد تعبئته⟩ |

## للاعتماد

يتحول إلى `ACTIVE` بعد أن يملأ الطبيب/ة الجدول أعلاه وتؤكد `last_verified`، ثم يُضاف إلى `used_by` في كل مساعد يستهلكه فعلياً عبر `knowledge_dependencies`.
