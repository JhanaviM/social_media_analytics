"""
Report Generation: Creates a professional PDF report for a case.
"""
import os
from datetime import datetime


def generate_pdf_report(case, results: dict) -> str:
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable, PageBreak
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT

        output_path = f'/tmp/{case.name.replace(" ", "_")}_report.pdf'
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                                rightMargin=0.75*inch, leftMargin=0.75*inch,
                                topMargin=1*inch, bottomMargin=0.75*inch)

        styles = getSampleStyleSheet()
        story = []

        # Custom styles
        title_style = ParagraphStyle('Title', parent=styles['Title'],
                                     fontSize=24, textColor=colors.HexColor('#6C63FF'),
                                     spaceAfter=6, alignment=TA_CENTER)
        h1_style = ParagraphStyle('H1', parent=styles['Heading1'],
                                   fontSize=16, textColor=colors.HexColor('#2D2D2D'),
                                   spaceBefore=16, spaceAfter=8)
        h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
                                   fontSize=13, textColor=colors.HexColor('#6C63FF'),
                                   spaceBefore=10, spaceAfter=6)
        body_style = ParagraphStyle('Body', parent=styles['Normal'],
                                     fontSize=11, leading=16, spaceAfter=6)
        kpi_style = ParagraphStyle('KPI', parent=styles['Normal'],
                                    fontSize=13, fontName='Helvetica-Bold',
                                    textColor=colors.HexColor('#6C63FF'))

        # Title page
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("Social Media Analytics Report", title_style))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#6C63FF')))
        story.append(Spacer(1, 0.2*inch))

        # Meta table
        meta = [
            ['Case Name', case.name],
            ['Keyword', case.keyword],
            ['Platform', case.platform],
            ['Generated', datetime.now().strftime('%Y-%m-%d %H:%M')],
            ['Description', case.description or 'N/A'],
        ]
        meta_table = Table(meta, colWidths=[1.5*inch, 4.5*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F0FF')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#6C63FF')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#FAFAFA')]),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.3*inch))

        # 1. Introduction
        story.append(Paragraph("1. Introduction", h1_style))
        story.append(Paragraph(
            f"This report presents a comprehensive social media analytics study on the topic of "
            f"<b>{case.keyword}</b> across <b>{case.platform}</b>. The analysis was conducted using "
            f"12 specialized AI/ML modules covering sentiment analysis, trend detection, network analysis, "
            f"influencer identification, and engagement prediction.",
            body_style
        ))

        # 2. Problem Statement
        story.append(Paragraph("2. Problem Statement", h1_style))
        story.append(Paragraph(
            "Social media platforms generate billions of data points daily. Understanding this data "
            "requires sophisticated AI tools that can process text, identify patterns, detect misinformation, "
            "and predict future trends. This project addresses that need by building a full-stack "
            "analytics platform integrating NLP, ML, and graph analysis.",
            body_style
        ))

        # 3. Case Study Description
        story.append(Paragraph("3. Case Study Description", h1_style))
        story.append(Paragraph(f"<b>Topic/Brand:</b> {case.keyword}", body_style))
        story.append(Paragraph(f"<b>Platform:</b> {case.platform}", body_style))
        story.append(Paragraph(f"<b>Analysis Goal:</b> Multi-dimensional analytics covering all 12 modules", body_style))

        # 4. System Architecture
        story.append(Paragraph("4. System Architecture", h1_style))
        story.append(Paragraph(
            "The system follows a full-stack MVC architecture: Flask backend with SQLAlchemy ORM, "
            "SQLite/PostgreSQL database, modular Python analytics engine, and a responsive HTML/JS "
            "frontend with Chart.js visualizations. Data is collected via Apify API or sample datasets.",
            body_style
        ))

        story.append(PageBreak())

        # 5. Module Results
        story.append(Paragraph("5. Analysis Results", h1_style))

        # Sentiment
        if 'sentiment' in results:
            s = results['sentiment']
            story.append(Paragraph("5.1 Sentiment Analysis", h2_style))
            if 'distribution' in s:
                dist = s['distribution']
                kpis = [
                    ['Positive', 'Negative', 'Neutral', 'Avg Score'],
                    [
                        str(dist.get('Positive', 0)),
                        str(dist.get('Negative', 0)),
                        str(dist.get('Neutral', 0)),
                        str(s.get('average_score', 0))
                    ]
                ]
                kpi_tbl = Table(kpis, colWidths=[1.5*inch]*4)
                kpi_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6C63FF')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
                    ('PADDING', (0, 0), (-1, -1), 8),
                ]))
                story.append(kpi_tbl)
                story.append(Spacer(1, 0.1*inch))

        # Trending
        if 'trending' in results:
            t = results['trending']
            story.append(Paragraph("5.2 Trending Topics", h2_style))
            top_tags = t.get('top_hashtags', [])[:5]
            if top_tags:
                tag_str = ', '.join(f"{tag['tag']} ({tag['count']})" for tag in top_tags)
                story.append(Paragraph(f"<b>Top Hashtags:</b> {tag_str}", body_style))

        # Influencers
        if 'influencer' in results:
            inf = results['influencer']
            story.append(Paragraph("5.3 Influencer Detection", h2_style))
            top_infs = inf.get('top_influencers', [])[:5]
            if top_infs:
                inf_data = [['Rank', 'Author', 'Influence Score', 'Followers', 'Tier']]
                for rank, inf_user in enumerate(top_infs, 1):
                    inf_data.append([
                        str(rank),
                        inf_user.get('author', ''),
                        str(inf_user.get('influence_score', 0)),
                        f"{inf_user.get('followers', 0):,}",
                        inf_user.get('tier', ''),
                    ])
                inf_table = Table(inf_data, colWidths=[0.5*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1.5*inch])
                inf_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#48CAE4')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('PADDING', (0, 0), (-1, -1), 6),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0FCFF')]),
                ]))
                story.append(inf_table)

        # Prediction
        if 'prediction' in results:
            pred = results['prediction']
            story.append(Paragraph("5.4 Popularity Prediction", h2_style))
            perf = pred.get('model_performance', {})
            story.append(Paragraph(
                f"<b>Best Model:</b> {perf.get('best_model', 'N/A')} | "
                f"<b>R² Score:</b> {perf.get('random_forest_r2', 0)} | "
                f"<b>RMSE:</b> {perf.get('random_forest_rmse', 0)}",
                body_style
            ))

        # Ads
        if 'ads' in results:
            ads = results['ads']
            story.append(Paragraph("5.5 Ad Campaign Optimization", h2_style))
            m = ads.get('metrics', {})
            if m:
                story.append(Paragraph(
                    f"<b>CTR:</b> {m.get('ctr', 0)}% | <b>ROI:</b> {m.get('roi', 0)}% | "
                    f"<b>Conversions:</b> {m.get('total_conversions', 0)} | "
                    f"<b>Grade:</b> {ads.get('performance_grade', 'N/A')}",
                    body_style
                ))

        story.append(PageBreak())

        # 6. Conclusion
        story.append(Paragraph("6. Conclusion", h1_style))
        story.append(Paragraph(
            f"This analytics report on <b>{case.keyword}</b> demonstrates the power of AI-driven "
            f"social media intelligence. By integrating 12 analytical modules, we were able to "
            f"extract actionable insights from raw social data — from understanding audience sentiment "
            f"to predicting viral content and optimizing ad campaigns.",
            body_style
        ))

        # 7. References
        story.append(Paragraph("7. References", h1_style))
        refs = [
            "NLTK — Natural Language Toolkit: https://www.nltk.org",
            "NetworkX — Network Analysis: https://networkx.org",
            "scikit-learn — Machine Learning: https://scikit-learn.org",
            "Apify — Web Scraping Platform: https://apify.com",
            "Flask — Python Web Framework: https://flask.palletsprojects.com",
        ]
        for ref in refs:
            story.append(Paragraph(f"• {ref}", body_style))

        # Footer
        story.append(Spacer(1, 0.5*inch))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#DDDDDD')))
        story.append(Paragraph(
            f"Generated by Social Media Analytics Platform | {datetime.now().strftime('%Y-%m-%d')}",
            ParagraphStyle('footer', parent=styles['Normal'], fontSize=9,
                           textColor=colors.grey, alignment=TA_CENTER)
        ))

        doc.build(story)
        return output_path

    except Exception as e:
        raise Exception(f"Report generation failed: {str(e)}")
