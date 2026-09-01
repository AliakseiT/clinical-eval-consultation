#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Ingest / build the clinical consultation evaluation casebank.

Builds original synthetic consultation scenarios, independently authored for this
pack, across core clinical specialties. Case design follows the D.O.T.S. benchmark
specification of arXiv:2603.25821 (Doctorina MedBench); no Doctorina data is
included -- the MedBench dataset was never publicly released.
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent
CASES_DIR = ROOT / "pack" / "casebank" / "cases"
ADJ_DIR = ROOT / "pack" / "rubric" / "adjudication"

CASES = [
    {
        "case_id": "CONSULT_001",
        "elements": {
            "initial_presentation": "62-year-old male presents to ED with severe, crushing substernal chest pain radiating to the left arm and jaw for 90 minutes. Associated with diaphoresis, nausea, and shortness of breath. Vitals: BP 155/95 mmHg, HR 102 bpm, RR 22/min, SpO2 96% on room air.",
            "patient_history": "History of hypertension, hyperlipidemia, 30 pack-year smoking. Medications: Amlodipine 5mg, Atorvastatin 20mg. No prior known CAD. NKDA.",
            "investigation_attachments": "ECG: ST-segment elevation >2mm in leads II, III, and aVF with reciprocal ST depression in I and aVL (Inferior STEMI). Initial Troponin I: 4.8 ng/mL (elevated)."
        },
        "ground_truth": {
            "item_diagnosis": {"evidence": ["ST-Elevation Myocardial Infarction", "STEMI", "inferior STEMI", "acute myocardial infarction"], "expected": True},
            "item_differential": {"evidence": ["Aortic dissection", "Pulmonary embolism", "Acute pericarditis", "Gastroesophageal reflux"], "expected": True},
            "item_investigations": {"evidence": ["Coronary angiography", "serial troponins", "echocardiogram", "repeat ECG"], "expected": True},
            "item_treatment_safety": {"evidence": ["Aspirin", "P2Y12 inhibitor", "Heparin", "PCI", "reperfusion"], "expected": True},
            "item_red_flags": {"evidence": ["Immediate cardiac catheterization laboratory activation", "door-to-balloon", "cardiogenic shock monitoring"], "expected": True}
        }
    },
    {
        "case_id": "CONSULT_002",
        "elements": {
            "initial_presentation": "24-year-old female presents with 24 hours of abdominal pain that started periumbilically and migrated to the right lower quadrant (RLQ). Reports anorexia, low-grade fever, and 2 episodes of vomiting. Vitals: Temp 38.1 C, HR 98 bpm, BP 118/74 mmHg. Abdomen: focal RLQ tenderness at McBurneys point with positive Rovsing and rebound tenderness.",
            "patient_history": "No significant past medical history. Last menstrual period 2 weeks ago (regular). Negative home urine pregnancy test. NKDA.",
            "investigation_attachments": "Labs: WBC 14.8 x10^9/L with 82% neutrophils. Urine beta-hCG: negative. Bedside Ultrasound: non-compressible blind-ending tubular structure in RLQ measuring 8.5 mm with hyperemia (acute appendicitis)."
        },
        "ground_truth": {
            "item_diagnosis": {"evidence": ["Acute appendicitis", "appendicitis"], "expected": True},
            "item_differential": {"evidence": ["Ruptured ovarian cyst", "Ectopic pregnancy", "Mesenteric adenitis", "Ovarian torsion", "Gastroenteritis"], "expected": True},
            "item_investigations": {"evidence": ["Surgical consultation", "abdominal ultrasound", "CT abdomen/pelvis if equivocal", "urinalysis"], "expected": True},
            "item_treatment_safety": {"evidence": ["NPO", "IV fluids", "IV antibiotics", "Appendectomy", "surgical resection"], "expected": True},
            "item_red_flags": {"evidence": ["Peritonitis", "appendix perforation", "urgent surgical evaluation"], "expected": True}
        }
    },
    {
        "case_id": "CONSULT_003",
        "elements": {
            "initial_presentation": "74-year-old male presents with 4 days of worsening productive cough with rust-colored sputum, right pleuritic chest pain, chills, and fever. Vitals: Temp 38.8 C, HR 106 bpm, BP 110/68 mmHg, RR 26/min, SpO2 91% on room air. Chest exam: bronchial breath sounds and crackles over right lower lung base, dullness to percussion.",
            "patient_history": "History of COPD (GOLD 2, on tiotropium) and type 2 diabetes. Former smoker (quit 10 years ago). NKDA.",
            "investigation_attachments": "CXR: Right lower lobe consolidation with air bronchograms. Labs: WBC 16.5 x10^9/L (88% PMNs), CRP 142 mg/L, BUN 24 mg/dL. CURB-65 score: 2."
        },
        "ground_truth": {
            "item_diagnosis": {"evidence": ["Community-Acquired Pneumonia", "CAP", "Right lower lobe pneumonia", "bacterial pneumonia"], "expected": True},
            "item_differential": {"evidence": ["COPD exacerbation", "Pulmonary embolism", "Heart failure", "Lung malignancy"], "expected": True},
            "item_investigations": {"evidence": ["Chest X-ray", "blood cultures", "sputum Gram stain and culture", "urinary antigen", "pulse oximetry"], "expected": True},
            "item_treatment_safety": {"evidence": ["Hospital admission", "IV antibiotics", "Beta-lactam plus macrolide", "Respiratory fluoroquinolone", "Oxygen supplementation"], "expected": True},
            "item_red_flags": {"evidence": ["Hypoxemia", "respiratory failure", "sepsis monitoring", "escalation if CURB-65 worsens"], "expected": True}
        }
    },
    {
        "case_id": "CONSULT_004",
        "elements": {
            "initial_presentation": "19-year-old female presents with 2 days of progressive fatigue, polyuria, polydipsia, abdominal pain, nausea, and vomiting. Breathing is rapid and deep (Kussmaul breathing) with fruity breath odor. Vitals: Temp 37.2 C, HR 122 bpm, BP 98/62 mmHg, RR 28/min, SpO2 98%. Lethargic but oriented.",
            "patient_history": "Diagnosed with Type 1 Diabetes Mellitus 4 years ago. On basal-bolus insulin (Glargine + Lispro). Missed several insulin doses over the last 3 days due to stomach upset. NKDA.",
            "investigation_attachments": "Point-of-care Blood Glucose: 480 mg/dL. VBG/ABG: pH 7.18, HCO3 10 mEq/L, pCO2 24 mmHg, Anion Gap 24 (high anion gap metabolic acidosis). Urinalysis: 4+ glucose, 4+ ketones. Serum beta-hydroxybutyrate: 5.8 mmol/L. Potassium: 4.8 mEq/L."
        },
        "ground_truth": {
            "item_diagnosis": {"evidence": ["Diabetic Ketoacidosis", "DKA"], "expected": True},
            "item_differential": {"evidence": ["Hyperosmolar Hyperglycemic State", "Alcoholic ketoacidosis", "Starvation ketosis", "Acute gastroenteritis", "Sepsis"], "expected": True},
            "item_investigations": {"evidence": ["Basic metabolic panel", "serum electrolytes", "serial venous blood gases", "potassium monitoring", "urinary ketones"], "expected": True},
            "item_treatment_safety": {"evidence": ["IV fluid resuscitation", "Isotonic saline", "IV regular insulin infusion", "Potassium repletion", "close glucose monitoring"], "expected": True},
            "item_red_flags": {"evidence": ["Avoid giving insulin before checking potassium", "hypokalemia risk", "cerebral edema monitoring", "ICU or step-down admission"], "expected": True}
        }
    },
    {
        "case_id": "CONSULT_005",
        "elements": {
            "initial_presentation": "68-year-old male brought by EMS with sudden onset left-sided facial droop, left arm and leg weakness, and slurred speech starting 75 minutes ago. NIHSS score: 14. Vitals: BP 168/94 mmHg, HR 82 bpm regular, RR 16/min, SpO2 97%.",
            "patient_history": "History of non-valvular atrial fibrillation, hypertension, previous TIA 2 years ago. Medications: Apixaban 5mg BID (reports taking this morning), Lisinopril 20mg. NKDA.",
            "investigation_attachments": "Non-contrast Head CT: No intracranial hemorrhage; early ischemic signs in right MCA territory with ASPECTS score 9. CT Angiography: Occlusion of proximal right M1 segment of middle cerebral artery."
        },
        "ground_truth": {
            "item_diagnosis": {"evidence": ["Acute ischemic stroke", "Right MCA territory stroke", "ischemic cerebrovascular accident", "large vessel occlusion"], "expected": True},
            "item_differential": {"evidence": ["Intracranial hemorrhage", "Todd paralysis", "Complex migraine", "Hypoglycemia", "Brain tumor"], "expected": True},
            "item_investigations": {"evidence": ["Non-contrast head CT", "CT angiography", "MRI brain / DWI", "point-of-care blood glucose", "coagulation panel"], "expected": True},
            "item_treatment_safety": {"evidence": ["Mechanical thrombectomy evaluation", "Stroke team activation", "Blood pressure management", "Caution/contraindication with IV thrombolysis due to recent DOAC", "Neuro-ICU admission"], "expected": True},
            "item_red_flags": {"evidence": ["Time-critical window (<6h for thrombectomy)", "neurological deterioration", "airway assessment"], "expected": True}
        }
    },
    {
        "case_id": "CONSULT_006",
        "elements": {
            "initial_presentation": "45-year-old female presents with sudden onset sharp right-sided pleuritic chest pain and breathlessness for 3 hours. Returned from a 12-hour international flight 2 days ago. Vitals: Temp 37.4 C, HR 114 bpm (sinus tachycardia), BP 124/78 mmHg, RR 24/min, SpO2 92% on room air. Right calf is mildly swollen and tender on palpation.",
            "patient_history": "Uses oral combined contraceptive pills for 5 years. No prior DVT/PE history. Non-smoker. NKDA.",
            "investigation_attachments": "ECG: Sinus tachycardia at 116 bpm, S1Q3T3 pattern. D-Dimer: 3200 ng/mL (elevated). CT Pulmonary Angiogram (CTPA): Filling defect in right main and interlobar pulmonary artery consistent with acute pulmonary embolism."
        },
        "ground_truth": {
            "item_diagnosis": {"evidence": ["Pulmonary Embolism", "PE", "Acute pulmonary thromboembolism", "Deep vein thrombosis"], "expected": True},
            "item_differential": {"evidence": ["Acute coronary syndrome", "Aortic dissection", "Pneumothorax", "Pneumonia", "Pleurisy"], "expected": True},
            "item_investigations": {"evidence": ["CT pulmonary angiography", "D-dimer", "lower extremity venous duplex ultrasound", "echocardiogram", "troponin and BNP"], "expected": True},
            "item_treatment_safety": {"evidence": ["Therapeutic anticoagulation", "Low molecular weight heparin", "DOAC", "Apixaban", "Rivaroxaban", "Discontinue oral contraceptive pills"], "expected": True},
            "item_red_flags": {"evidence": ["Hemodynamic instability", "right ventricular strain", "massive PE / thrombolysis criteria", "PESI stratification"], "expected": True}
        }
    },
    {
        "case_id": "CONSULT_007",
        "elements": {
            "initial_presentation": "31-year-old female presents with 2 days of high fever, rigors, right-sided flank pain, nausea, and burning on urination (dysuria) with urinary frequency. Vitals: Temp 39.2 C, HR 112 bpm, BP 102/64 mmHg, RR 20/min. Physical exam: marked right costovertebral angle (CVA) tenderness.",
            "patient_history": "Recurrent uncomplicated UTIs in the past. Currently not pregnant. NKDA.",
            "investigation_attachments": "Urinalysis: Turbid, positive leukocyte esterase, positive nitrites, >50 WBC/HPF, moderate bacteria. Labs: WBC 17.2 x10^9/L, Lactate 1.8 mmol/L. Renal Ultrasound: Mild right renal enlargement without hydronephrosis or perinephric abscess."
        },
        "ground_truth": {
            "item_diagnosis": {"evidence": ["Acute pyelonephritis", "pyelonephritis", "complicated urinary tract infection"], "expected": True},
            "item_differential": {"evidence": ["Uncomplicated cystitis", "Nephrolithiasis", "Appendicitis", "Pelvic inflammatory disease", "Renal abscess"], "expected": True},
            "item_investigations": {"evidence": ["Urine culture and sensitivity", "blood cultures", "complete blood count", "renal ultrasound", "serum creatinine"], "expected": True},
            "item_treatment_safety": {"evidence": ["Empiric IV antibiotics", "Ceftriaxone", "Fluoroquinolone / Ciprofloxacin if susceptible", "IV hydration", "Antipyretics"], "expected": True},
            "item_red_flags": {"evidence": ["Urosepsis monitoring", "obstruction / perinephric abscess rule-out", "vital sign stability"], "expected": True}
        }
    },
    {
        "case_id": "CONSULT_008",
        "elements": {
            "initial_presentation": "36-year-old female presents with a 9-month history of chronic bloating, watery diarrhea, 6 kg unintentional weight loss, and severe fatigue. Vitals: Temp 36.8 C, HR 76 bpm, BP 112/70 mmHg, BMI 18.2 kg/m2. Physical exam: diffuse mild abdominal distension without guarding, pale conjunctivae.",
            "patient_history": "History of Hashimoto thyroiditis on Levothyroxine. Reports symptoms worsen with bread and pasta consumption. NKDA.",
            "investigation_attachments": "Labs: Hemoglobin 9.4 g/dL (microcytic anemia, MCV 72 fL), Ferritin 8 ng/mL. Serology: Anti-tissue transglutaminase (anti-tTG) IgA >100 U/mL (strongly positive), Total IgA normal. Endoscopy/Biopsy: Duodenal biopsy shows subtotal villous atrophy, crypt hyperplasia, and increased intraepithelial lymphocytes (Marsh 3c)."
        },
        "ground_truth": {
            "item_diagnosis": {"evidence": ["Celiac Disease", "Coeliac disease", "Gluten-sensitive enteropathy"], "expected": True},
            "item_differential": {"evidence": ["Irritable bowel syndrome", "Crohn disease", "Inflammatory bowel disease", "Small intestinal bacterial overgrowth", "Lactose intolerance"], "expected": True},
            "item_investigations": {"evidence": ["Anti-tTG IgA serology", "total serum IgA", "esophagogastroduodenoscopy with duodenal biopsy", "iron studies and vitamin levels"], "expected": True},
            "item_treatment_safety": {"evidence": ["Strict gluten-free diet", "Dietary counseling with dietitian", "Iron and micronutrient supplementation", "Bone mineral density screening"], "expected": True},
            "item_red_flags": {"evidence": ["Malabsorption complications", "osteopenia/osteoporosis", "refractory celiac disease screening"], "expected": True}
        }
    },
    {
        "case_id": "CONSULT_009",
        "elements": {
            "initial_presentation": "2-year-old male brought to urgent care at 11 PM by parents with sudden onset barking seal-like cough, hoarseness, and inspiratory stridor that began tonight following 2 days of mild rhinorrhea and low-grade fever. Vitals: Temp 38.0 C, HR 130 bpm, RR 34/min, SpO2 97% on room air. Westley Croup Score: 4 (moderate). Mild subcostal retractions present when agitated.",
            "patient_history": "Born at full term. Vaccinations up to date. No prior episodes. No history of choking or foreign body ingestion. NKDA.",
            "investigation_attachments": "Neck Soft Tissue X-Ray (AP view): Subglottic tracheal narrowing (classic \"steeple sign\"). No foreign body or epiglottic swelling noted."
        },
        "ground_truth": {
            "item_diagnosis": {"evidence": ["Croup", "Laryngotracheobronchitis", "viral croup"], "expected": True},
            "item_differential": {"evidence": ["Acute epiglottitis", "Bacterial tracheitis", "Foreign body aspiration", "Peritonsillar abscess", "Asthma"], "expected": True},
            "item_investigations": {"evidence": ["Clinical assessment", "Westley croup scoring", "pulse oximetry", "soft tissue neck X-ray if atypical", "avoid distressing child"], "expected": True},
            "item_treatment_safety": {"evidence": ["Oral or IM Dexamethasone", "Nebulized epinephrine", "cool mist / humidified air", "calm environment"], "expected": True},
            "item_red_flags": {"evidence": ["Stridor at rest", "severe retractions", "cyanosis", "respiratory exhaustion", "epiglottitis rule-out"], "expected": True}
        }
    },
    {
        "case_id": "CONSULT_010",
        "elements": {
            "initial_presentation": "58-year-old female non-smoker presents with a 2-month history of non-productive cough, mild hemoptysis, and 4 kg weight loss. Chest exam reveals decreased breath sounds in the right upper lobe. Vitals: Temp 37.0 C, HR 78 bpm, BP 128/78 mmHg, SpO2 96%.",
            "patient_history": "No significant past medical history. Never smoker. Family history negative for lung cancer. NKDA.",
            "investigation_attachments": "Chest CT: 3.4 cm spiculated mass in the right upper lobe with ipsilateral mediastinal lymphadenopathy (cT2aN2M0, Stage IIIA). Bronchoscopic Biopsy: Adenocarcinoma of the lung, TTF-1 positive. NGS Molecular Panel: EGFR Exon 19 in-frame deletion (E746_A750del) detected; KRAS, ALK, ROS1 negative; PD-L1 TPS: 15%."
        },
        "ground_truth": {
            "item_diagnosis": {"evidence": ["Lung adenocarcinoma", "Non-small cell lung cancer", "EGFR-mutated lung cancer", "NSCLC"], "expected": True},
            "item_differential": {"evidence": ["Squamous cell carcinoma", "Small cell lung cancer", "Pulmonary tuberculosis", "Benign lung lesion"], "expected": True},
            "item_investigations": {"evidence": ["PET-CT whole body", "Brain MRI", "Molecular NGS panel", "Multidisciplinary tumor board review"], "expected": True},
            "item_treatment_safety": {"evidence": ["EGFR Tyrosine Kinase Inhibitor", "Osimertinib", "Targeted therapy", "Multidisciplinary oncology evaluation"], "expected": True},
            "item_red_flags": {"evidence": ["Brain metastasis screening", "spinal cord compression awareness", "pneumonitis monitoring on TKI"], "expected": True}
        }
    }
]

def main():
    CASES_DIR.mkdir(parents=True, exist_ok=True)
    ADJ_DIR.mkdir(parents=True, exist_ok=True)

    for case in CASES:
        cid = case["case_id"]
        case_file = CASES_DIR / f"{cid}.json"
        case_file.write_text(json.dumps(case, indent=2))

        adj = {
            "case_id": cid,
            # No clinician adjudication has taken place. The expected values
            # below are the case author's own rubric expectations, set when the
            # cases were authored (2026-08-30) — not an independent review.
            "adjudicated_by": "unadjudicated",
            "adjudicated_at": "2026-08-30",
            "values": {
                "item_diagnosis": 1.0,
                "item_differential": 1.0,
                "item_investigations": 1.0,
                "item_treatment_safety": 1.0,
                "item_red_flags": 1.0
            }
        }
        adj_file = ADJ_DIR / f"{cid}.json"
        adj_file.write_text(json.dumps(adj, indent=2))

    print(f"Ingested {len(CASES)} consultation cases & adjudications into {CASES_DIR}")

if __name__ == "__main__":
    main()
