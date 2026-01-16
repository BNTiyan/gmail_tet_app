"""
Telugu Daily Horoscope Email Automation with Dynamic Predictions
Based on Planetary Movements and Panchang Data
"""

import datetime
import smtplib
import os
import json
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Tuple
import math


class PanchangCalculator:
    """Calculate Telugu Panchang elements"""
    
    def __init__(self):
        self.tithis = [
            "పాడ్యమి", "విదియ", "తదియ", "చవితి", "పంచమి",
            "షష్టి", "సప్తమి", "అష్టమి", "నవమి", "దశమి",
            "ఏకాదశి", "ద్వాదశి", "త్రయోదశి", "చతుర్దశి", "పౌర్ణమి/అమావాస్య"
        ]
        
        self.nakshatras = [
            "అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర",
            "ఆరుద్ర", "పునర్వసు", "పుష్యమి", "ఆశ్లేష", "మఖ",
            "పుబ్బ", "ఉత్తర", "హస్త", "చిత్త", "స్వాతి",
            "విశాఖ", "అనూరాధ", "జ్యేష్ఠ", "మూల", "పూర్వాషాఢ",
            "ఉత్తరాషాఢ", "శ్రవణం", "ధనిష్ఠ", "శతభిషం", "పూర్వాభాద్ర",
            "ఉత్తరాభాద్ర", "రేవతి"
        ]
        
        self.weekdays_telugu = {
            0: "సోమవారం", 1: "మంగళవారం", 2: "బుధవారం",
            3: "గురువారం", 4: "శుక్రవారం", 5: "శనివారం", 6: "ఆదివారం"
        }
    
    def get_tithi(self, date: datetime.date) -> str:
        """Calculate Tithi (lunar day) - simplified calculation"""
        # Calculate days since reference new moon
        reference_date = datetime.date(2024, 1, 11)  # Amavasya
        days_diff = (date - reference_date).days
        lunar_day = (days_diff % 30)
        
        paksha = "శుక్ల పక్షం" if lunar_day < 15 else "కృష్ణ పక్షం"
        tithi_index = lunar_day % 15
        
        return f"{paksha} {self.tithis[tithi_index]}"
    
    def get_nakshatra(self, date: datetime.date) -> str:
        """Calculate Nakshatra - simplified calculation"""
        days_since_epoch = (date - datetime.date(2000, 1, 1)).days
        nakshatra_index = (days_since_epoch * 13) % 27
        return self.nakshatras[nakshatra_index]
    
    def get_moon_phase(self, date: datetime.date) -> str:
        """Get moon phase"""
        reference_date = datetime.date(2024, 1, 11)
        days_diff = (date - reference_date).days
        phase = (days_diff % 30) / 30
        
        if phase < 0.03 or phase > 0.97:
            return "అమావాస్య (New Moon)"
        elif 0.22 < phase < 0.28:
            return "పూర్తి చంద్రుడు (Full Moon)"
        elif phase < 0.25:
            return "వర్ధమాన చంద్రుడు (Waxing)"
        else:
            return "క్షీణించు చంద్రుడు (Waning)"
    
    def get_weekday_telugu(self, date: datetime.date) -> str:
        """Get Telugu weekday name"""
        return self.weekdays_telugu[date.weekday()]


class DynamicPredictionEngine:
    """Generate dynamic predictions based on planetary positions"""
    
    def __init__(self):
        self.panchang = PanchangCalculator()
        
        # Base characteristics for each rashi
        self.rashi_base = {
            "వృషభం": {
                "element": "earth",
                "lord": "venus",
                "nature": "fixed",
                "favorable_days": [4, 5],  # Thursday, Friday
                "areas": ["finance", "family", "comfort", "relationships"]
            },
            "సింహం": {
                "element": "fire",
                "lord": "sun",
                "nature": "fixed",
                "favorable_days": [6],  # Sunday
                "areas": ["leadership", "career", "recognition", "authority"]
            },
            "ధనుస్సు": {
                "element": "fire",
                "lord": "jupiter",
                "nature": "dual",
                "favorable_days": [3],  # Thursday
                "areas": ["education", "travel", "spirituality", "fortune"]
            },
            "మేషం": {
                "element": "fire",
                "lord": "mars",
                "nature": "movable",
                "favorable_days": [1, 6],
                "areas": ["action", "courage", "initiative", "competition"]
            },
            "మిథునం": {
                "element": "air",
                "lord": "mercury",
                "nature": "dual",
                "favorable_days": [2],
                "areas": ["communication", "learning", "networking", "versatility"]
            },
            "కర్కాటకం": {
                "element": "water",
                "lord": "moon",
                "nature": "movable",
                "favorable_days": [0],
                "areas": ["emotions", "home", "family", "nurturing"]
            },
            "కన్య": {
                "element": "earth",
                "lord": "mercury",
                "nature": "dual",
                "favorable_days": [2],
                "areas": ["service", "health", "analysis", "perfection"]
            },
            "తుల": {
                "element": "air",
                "lord": "venus",
                "nature": "movable",
                "favorable_days": [4],
                "areas": ["relationships", "balance", "art", "harmony"]
            },
            "వృశ్చికం": {
                "element": "water",
                "lord": "mars",
                "nature": "fixed",
                "favorable_days": [1],
                "areas": ["transformation", "intensity", "secrets", "power"]
            },
            "మకరం": {
                "element": "earth",
                "lord": "saturn",
                "nature": "movable",
                "favorable_days": [5],
                "areas": ["discipline", "career", "ambition", "responsibility"]
            },
            "కుంభం": {
                "element": "air",
                "lord": "saturn",
                "nature": "fixed",
                "favorable_days": [5],
                "areas": ["innovation", "social", "freedom", "uniqueness"]
            },
            "మీనం": {
                "element": "water",
                "lord": "jupiter",
                "nature": "dual",
                "favorable_days": [3],
                "areas": ["spirituality", "compassion", "intuition", "dreams"]
            }
        }
        
        # Prediction templates based on different factors
        self.prediction_templates = {
            "favorable": [
                "ఈరోజు మీకు అనుకూలమైన రోజు. {area}లో మంచి పురోగతి ఉంటుంది.",
                "{area} విషయాలలో విజయం సాధించే అవకాశాలు ఉన్నాయి.",
                "ఈరోజు {area}కు సంబంధించిన కార్యక్రమాలు శుభఫలితాలిస్తాయి.",
            ],
            "neutral": [
                "{area} విషయాలలో సాధారణ పరిస్థితులు ఉంటాయి. జాగ్రత్తగా ముందుకు సాగండి.",
                "ఈరోజు {area}లో ఓపిక పాటించండి. మంచి ఫలితాలు రావొచ్చు.",
            ],
            "challenging": [
                "{area} విషయాలలో జాగ్రత్త అవసరం. త్వరపడకుండా నిర్ణయాలు తీసుకోండి.",
                "ఈరోజు {area}లో అడ్డంకులు ఎదురవొచ్చు. ధైర్యంగా ఎదుర్కోండి.",
            ]
        }
    
    def generate_daily_prediction(self, rashi: str, date: datetime.date) -> Dict:
        """Generate dynamic prediction based on date and rashi"""
        
        # Get panchang data
        tithi = self.panchang.get_tithi(date)
        nakshatra = self.panchang.get_nakshatra(date)
        weekday = date.weekday()
        weekday_telugu = self.panchang.get_weekday_telugu(date)
        moon_phase = self.panchang.get_moon_phase(date)
        
        # Get rashi characteristics
        rashi_info = self.rashi_base.get(rashi, self.rashi_base["మేషం"])
        
        # Calculate favorability score based on multiple factors
        favorability_score = 0
        
        # Check if today is favorable day for this rashi
        if weekday in rashi_info["favorable_days"]:
            favorability_score += 3
        
        # Date-based seed for daily variation
        date_seed = int(hashlib.md5(str(date).encode()).hexdigest()[:8], 16)
        day_influence = (date_seed % 10) - 5  # -5 to +4
        favorability_score += day_influence
        
        # Nakshatra influence
        nakshatra_index = self.panchang.nakshatras.index(nakshatra)
        if nakshatra_index % 3 == 0:
            favorability_score += 1
        
        # Generate prediction based on favorability
        if favorability_score >= 3:
            tone = "favorable"
        elif favorability_score <= -2:
            tone = "challenging"
        else:
            tone = "neutral"
        
        # Build detailed prediction
        prediction_parts = []
        
        # Opening based on weekday
        weekday_openings = {
            0: "సోమవారం చంద్రుని ప్రభావంతో మీ మనస్సు స్థిరంగా ఉంటుంది.",
            1: "మంగళవారం మంగళుని శక్తితో మీకు ధైర్యం, శక్తి లభిస్తాయి.",
            2: "బుధవారం బుధుని ఆశీస్సుతో మీ కమ్యూనికేషన్ నైపుణ్యాలు మెరుగుపడతాయి.",
            3: "గురువారం బృహస్పతి దేవుని కృపతో జ్ఞానం, అదృష్టం పెరుగుతాయి.",
            4: "శుక్రవారం శుక్రుని ప్రభావంతో సంబంధాలు, సౌందర్యం పెరుగుతాయి.",
            5: "శనివారం శని దేవుని ప్రభావంతో కష్టపడి పనిచేయండి.",
            6: "ఆదివారం సూర్యదేవుని తేజస్సుతో మీ వ్యక్తిత్వం ప్రకాశిస్తుంది."
        }
        prediction_parts.append(weekday_openings[weekday])
        
        # Add area-specific predictions
        for area in rashi_info["areas"][:2]:  # Pick 2 main areas
            area_telugu = {
                "finance": "ఆర్థిక", "family": "కుటుంబ", "career": "వృత్తి",
                "education": "విద్యా", "health": "ఆరోగ్య", "relationships": "సంబంధ",
                "leadership": "నాయకత్వ", "spirituality": "ఆధ్యాత్మిక",
                "travel": "ప్రయాణ", "communication": "సంభాషణ",
                "action": "కార్య", "service": "సేవా", "balance": "సమతుల్యత",
                "transformation": "పరివర్తన", "discipline": "క్రమశిక్షణ",
                "innovation": "ఆవిష్కరణ", "compassion": "కరుణ"
            }.get(area, area)
            
            template = self.prediction_templates[tone][date_seed % len(self.prediction_templates[tone])]
            prediction_parts.append(template.format(area=area_telugu))
        
        # Add nakshatra influence
        nakshatra_effects = {
            "అశ్విని": "వేగవంతమైన పురోగతి",
            "రోహిణి": "స్థిరత్వం మరియు వృద్ధి",
            "పుష్యమి": "పోషణ మరియు శ్రేయస్సు",
            "మఖ": "గౌరవం మరియు అధికారం",
            "హస్త": "నైపుణ్యం మరియు సృజనాత్మకత",
            "స్వాతి": "స్వతంత్రత మరియు సానుకూలత",
            "అనూరాధ": "స్నేహం మరియు సహకారం",
            "మూల": "పరివర్తన మరియు పునాదులు",
            "శ్రవణం": "జ్ఞానం మరియు అవగాహన",
            "శతభిషం": "వైద్యం మరియు రహస్యాలు",
            "రేవతి": "కరుణ మరియు పూర్ణత్వం"
        }
        if nakshatra in nakshatra_effects:
            prediction_parts.append(f"{nakshatra} నక్షత్రం {nakshatra_effects[nakshatra]} తెస్తుంది.")
        
        # Moon phase influence
        if "పూర్తి చంద్రుడు" in moon_phase:
            prediction_parts.append("పౌర్ణమి యొక్క ప్రభావం మీ భావోద్వేగాలను బలపరుస్తుంది.")
        elif "అమావాస్య" in moon_phase:
            prediction_parts.append("అమావాస్య సమయం కొత్త ప్రారంభాలకు శుభం.")
        
        full_prediction = " ".join(prediction_parts)
        
        # Generate remedies based on weekday and rashi
        remedies = self.generate_daily_remedies(rashi, weekday, tone)
        
        # Lucky elements
        lucky_data = self.generate_lucky_elements(rashi, date, favorability_score)
        
        return {
            "prediction": full_prediction,
            "panchang": {
                "tithi": tithi,
                "nakshatra": nakshatra,
                "weekday": weekday_telugu,
                "moon_phase": moon_phase
            },
            **lucky_data,
            "remedies": remedies,
            "favorability": "అనుకూలం" if favorability_score >= 3 else "జాగ్రత్త" if favorability_score <= -2 else "సాధారణం"
        }
    
    def generate_daily_remedies(self, rashi: str, weekday: int, tone: str) -> List[str]:
        """Generate remedies based on weekday and conditions"""
        remedies = []
        
        # Weekday-specific remedies
        weekday_remedies = {
            0: ["సోమవారం శివుడిని పూజించండి", "పాల దానం చేయండి", "తెల్ల వస్తువులు ధరించండి"],
            1: ["మంగళవారం హనుమాన్ జీ పూజ", "ఎరుపు గింజలు దానం", "హనుమాన్ చాలీసా పారాయణ"],
            2: ["బుధవారం విష్ణు మూర్తిని పూజించండి", "పచ్చి మిరప దానం", "విద్యార్థులకు సహాయం"],
            3: ["గురువారం బృహస్పతి దేవుడిని పూజించండి", "పసుపు దానం", "గురువులను గౌరవించండి"],
            4: ["శుక్రవారం మహాలక్ష్మి పూజ", "తేనె దానం", "తెల్ల పూలు అర్పించండి"],
            5: ["శనివారం శని దేవుడిని నమస్కరించండి", "నల్లగింజలు దానం", "పేదలకు సహాయం"],
            6: ["ఆదివారం సూర్యుడికి అర్ఘ్యం", "గోధుమలు దానం", "పితృదేవతలకు ప్రార్థన"]
        }
        
        remedies.extend(weekday_remedies[weekday][:2])
        
        # Rashi-specific remedy
        rashi_remedies = {
            "వృషభం": "శుక్ర మంత్రం (ఓం శుక్రాయ నమః) జపించండి",
            "సింహం": "గాయత్రీ మంత్రం పారాయణ చేయండి",
            "ధనుస్సు": "విష్ణు సహస్రనామం చదవండి"
        }
        if rashi in rashi_remedies:
            remedies.append(rashi_remedies[rashi])
        
        # Condition-based remedy
        if tone == "challenging":
            remedies.append("ఈరోజు మీ ఇష్టదైవాన్ని ప్రార్థించండి - అడ్డంకులు తొలగిపోతాయి")
        
        return remedies
    
    def generate_lucky_elements(self, rashi: str, date: datetime.date, score: int) -> Dict:
        """Generate daily lucky elements"""
        
        date_seed = int(hashlib.md5(str(date).encode()).hexdigest()[:8], 16)
        
        # Base colors for each rashi
        rashi_colors = {
            "వృషభం": ["తెలుపు", "గులాబీ", "ఆకుపచ్చ"],
            "సింహం": ["బంగారు", "నారింజ", "ఎరుపు"],
            "ధనుస్సు": ["పసుపు", "నారింజ", "ఊదా"],
            "మేషం": ["ఎరుపు", "నారింజ"],
            "మిథునం": ["ఆకుపచ్చ", "పసుపు"],
            "కర్కాటకం": ["తెలుపు", "వెండి"],
            "కన్య": ["ఆకుపచ్చ", "గోధుమ"],
            "తుల": ["గులాబీ", "నీలం"],
            "వృశ్చికం": ["ఎరుపు", "నలుపు"],
            "మకరం": ["నలుపు", "గోధుమ"],
            "కుంభం": ["నీలం", "వైలెట్"],
            "మీనం": ["పసుపు", "సముద్ర ఆకుపచ్చ"]
        }
        
        colors = rashi_colors.get(rashi, ["తెలుపు"])
        lucky_color = colors[date_seed % len(colors)]
        
        # Lucky number based on date and score
        base_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        lucky_number = str(base_numbers[(date.day + score) % 9])
        
        # Lucky time
        time_slots = [
            "ఉదయం 6:00 - 9:00",
            "ఉదయం 10:00 - 12:00",
            "మధ్యాహ్నం 12:00 - 3:00",
            "సాయంత్రం 4:00 - 6:00",
            "సాయంత్రం 6:00 - 8:00"
        ]
        lucky_time = time_slots[date_seed % len(time_slots)]
        
        # Lucky direction
        directions = ["తూర్పు", "పడమర", "ఉత్తరం", "దక్షిణం", "ఈశాన్యం"]
        lucky_direction = directions[date_seed % len(directions)]
        
        return {
            "lucky_color": lucky_color,
            "lucky_number": lucky_number,
            "lucky_time": lucky_time,
            "lucky_direction": lucky_direction
        }


class TeluguHoroscopeSystem:
    """Main horoscope system with dynamic predictions"""
    
    def __init__(self):
        self.prediction_engine = DynamicPredictionEngine()
        self.panchang = PanchangCalculator()
        
        self.rashi_mapping = {
            "మేషం": "Aries", "వృషభం": "Taurus", "మిథునం": "Gemini",
            "కర్కాటకం": "Cancer", "సింహం": "Leo", "కన్య": "Virgo",
            "తుల": "Libra", "వృశ్చికం": "Scorpio", "ధనుస్సు": "Sagittarius",
            "మకరం": "Capricorn", "కుంభం": "Aquarius", "మీనం": "Pisces"
        }
    
    def calculate_rashi_from_dob(self, dob: datetime.date) -> str:
        """Calculate Telugu Rashi based on date of birth"""
        month, day = dob.month, dob.day
        
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "మేషం"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "వృషభం"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "మిథునం"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "కర్కాటకం"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "సింహం"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "కన్య"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "తుల"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "వృశ్చికం"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "ధనుస్సు"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "మకరం"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "కుంభం"
        else:
            return "మీనం"
    
    def generate_email_body(self, name: str, rashi: str, date: datetime.date) -> str:
        """Generate HTML email with dynamic predictions"""
        
        # Get dynamic prediction for today
        prediction_data = self.prediction_engine.generate_daily_prediction(rashi, date)
        panchang_data = prediction_data['panchang']
        
        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Noto Sans Telugu', Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; }}
                .container {{ max-width: 650px; margin: 20px auto; background: white; padding: 0; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 32px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }}
                .rashi-name {{ font-size: 36px; font-weight: bold; margin: 15px 0 10px 0; }}
                .date {{ font-size: 16px; opacity: 0.95; }}
                .favorability {{ display: inline-block; margin-top: 10px; padding: 8px 20px; background: rgba(255,255,255,0.2); border-radius: 20px; font-weight: bold; }}
                .content {{ padding: 30px; }}
                .greeting {{ font-size: 20px; color: #333; margin-bottom: 20px; }}
                .panchang {{ background: #fff9e6; padding: 20px; border-radius: 10px; margin-bottom: 25px; border-left: 5px solid #ffc107; }}
                .panchang h3 {{ margin: 0 0 15px 0; color: #f57c00; font-size: 20px; }}
                .panchang-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
                .panchang-item {{ background: white; padding: 12px; border-radius: 6px; }}
                .panchang-label {{ font-size: 13px; color: #666; margin-bottom: 5px; }}
                .panchang-value {{ font-size: 16px; font-weight: bold; color: #333; }}
                .section {{ margin: 25px 0; padding: 20px; background: #f8f9fa; border-radius: 10px; }}
                .section-title {{ color: #667eea; font-weight: bold; font-size: 20px; margin-bottom: 15px; display: flex; align-items: center; }}
                .section-title::before {{ content: ''; width: 4px; height: 24px; background: #667eea; margin-right: 10px; border-radius: 2px; }}
                .prediction {{ font-size: 17px; line-height: 1.8; color: #333; text-align: justify; }}
                .lucky-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 15px; }}
                .lucky-item {{ background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%); padding: 15px; border-radius: 10px; text-align: center; }}
                .lucky-label {{ font-size: 13px; color: #666; margin-bottom: 5px; }}
                .lucky-value {{ font-size: 18px; font-weight: bold; color: #1976d2; }}
                .remedies {{ list-style: none; padding: 0; margin: 0; }}
                .remedies li {{ padding: 15px; margin: 10px 0; background: linear-gradient(to right, #fff3e0 0%, #ffe0b2 100%); border-left: 4px solid #ff9800; border-radius: 6px; display: flex; align-items: start; }}
                .remedies li::before {{ content: '🔸'; margin-right: 10px; font-size: 18px; }}
                .footer {{ text-align: center; padding: 30px; background: #f8f9fa; border-top: 2px solid #e0e0e0; }}
                .footer p {{ margin: 10px 0; color: #666; }}
                .footer .blessing {{ font-size: 20px; color: #667eea; font-weight: bold; }}
                @media (max-width: 600px) {{
                    .lucky-grid {{ grid-template-columns: 1fr; }}
                    .panchang-grid {{ grid-template-columns: 1fr; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌟 రోజువారీ రాశి ఫలాలు 🌟</h1>
                    <div class="rashi-name">{rashi}</div>
                    <div class="date">{date.strftime('%d-%m-%Y')} | {panchang_data['weekday']}</div>
                    <div class="favorability">రోజు స్వభావం: {prediction_data['favorability']}</div>
                </div>
                
                <div class="content">
                    <p class="greeting">నమస్కారం {name} గారు,</p>
                    
                    <div class="panchang">
                        <h3>📅 ఈరోజు పంచాంగం</h3>
                        <div class="panchang-grid">
                            <div class="panchang-item">
                                <div class="panchang-label">తిథి</div>
                                <div class="panchang-value">{panchang_data['tithi']}</div>
                            </div>
                            <div class="panchang-item">
                                <div class="panchang-label">నక్షత్రం</div>
                                <div class="panchang-value">{panchang_data['nakshatra']}</div>
                            </div>
                            <div class="panchang-item">
                                <div class="panchang-label">వారం</div>
                                <div class="panchang-value">{panchang_data['weekday']}</div>
                            </div>
                            <div class="panchang-item">
                                <div class="panchang-label">చంద్ర స్థితి</div>
                                <div class="panchang-value">{panchang_data['moon_phase']}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="section">
                        <div class="section-title">📖 ఈరోజు మీ రాశి ఫలితం</div>
                        <p class="prediction">{prediction_data['prediction']}</p>
                    </div>
                    
                    <div class="section">
                        <div class="section-title">✨ అదృష్ట సంకేతాలు</div>
                        <div class="lucky-grid">
                            <div class="lucky-item">
                                <div class="lucky-label">🎨 రంగు</div>
                                <div class="lucky-value">{prediction_data['lucky_color']}</div>
                            </div>
                            <div class="lucky-item">
                                <div class="lucky-label">🔢 సంఖ్య</div>
                                <div class="lucky-value">{prediction_data['lucky_number']}</div>
                            </div>
                            <div class="lucky-item">
                                <div class="lucky-label">⏰ సమయం</div>
                                <div class="lucky-value">{prediction_data['lucky_time']}</div>
                            </div>
                            <div class="lucky-item">
                                <div class="lucky-label">🧭 దిశ</div>
                                <div class="lucky-value">{prediction_data['lucky_direction']}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="section">
                        <div class="section-title">🙏 ఈరోజు చేయవలసిన పరిహారాలు</div>
                        <ul class="remedies">
        """
        
        for remedy in prediction_data['remedies']:
            html += f"<li>{remedy}</li>"
        
        html += f"""
                        </ul>
                    </div>
                </div>
                
                <div class="footer">
                    <p class="blessing">శుభోదయం! మీ రోజు శుభంగా గడవాలని కోరుకుంటున్నాము 🌺</p>
                    <p style="margin-top: 15px; font-size: 13px; color: #999;">
                        <em>ఈ రాశి ఫలాలు పంచాంగం మరియు గ్రహ స్థానాల ఆధారంగా రోజువారీ మారుతాయి.<br/>
                        వ్యక్తిగత జాతక విశ్లేషణ కోసం అనుభవజ్ఞులైన జ్యోతిష్యుడిని సంప్రదించండి.</em>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def send_email(self, sender_email: str, sender_password: str, 
                   receiver_email: str, subject: str, html_content: str):
        """Send email using Gmail SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
            
            print(f"✅ Email sent successfully to {receiver_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False
    
    def send_daily_horoscopes(self, users: List[Dict], sender_email: str, sender_password: str):
        """Send horoscopes to all users with dynamic predictions"""
        today = datetime.date.today()
        success_count = 0
        
        print(f"🗓️  Generating predictions for {today.strftime('%d-%m-%Y')}")
        print(f"📧 Processing {len(users)} user(s)...\n")
        
        for user in users:
            try:
                name = user['name']
                email = user['email']
                rashi = user['rashi']
                
                # Validate rashi
                if rashi not in self.rashi_mapping:
                    print(f"⚠️  Invalid rashi '{rashi}' for {name}, skipping...")
                    continue
                
                print(f"📝 Generating prediction for {name} ({rashi})...")
                
                # Generate email content with dynamic predictions
                subject = f"🌟 {today.strftime('%d-%m-%Y')} - రోజువారీ రాశి ఫలాలు - {rashi}"
                html_content = self.generate_email_body(name, rashi, today)
                
                # Send email
                if self.send_email(sender_email, sender_password, email, subject, html_content):
                    success_count += 1
                    
            except KeyError as e:
                print(f"❌ Missing required field {e} for user {user.get('email', 'unknown')}")
            except Exception as e:
                print(f"❌ Error processing user {user.get('email', 'unknown')}: {str(e)}")
        
        print(f"\n📊 Summary: {success_count}/{len(users)} emails sent successfully")
        return success_count


def main():
    """Main function for GitHub Actions"""
    print("=" * 60)
    print("🚀 Telugu Daily Horoscope Service with Dynamic Predictions")
    print("=" * 60)
    
    # Get environment variables
    sender_email = os.environ.get('GMAIL_ADDRESS')
    sender_password = os.environ.get('GMAIL_APP_PASSWORD')
    users_json = 'USERS_JSON.json'
    
    if not sender_email or not sender_password:
        print("❌ Error: GMAIL_ADDRESS and GMAIL_APP_PASSWORD must be set")
        return
    
    # Parse users from JSON
    try:
        users = json.load(open(users_json, 'r'))
        if not users:
            print("❌ Error: No users configured in USERS_JSON")
            return
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing USERS_JSON: {str(e)}")
        return
    
    # Initialize and send
    horoscope_system = TeluguHoroscopeSystem()
    horoscope_system.send_daily_horoscopes(users, sender_email, sender_password)
    
    print("\n✅ Telugu Horoscope Email Service completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()