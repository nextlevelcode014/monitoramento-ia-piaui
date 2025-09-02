def generate_statistical_report(df, summary):
    if df is None or len(df) == 0:
        return None

    stats = {
        "total_news": len(df),
        "date_range": {"start": df["pub_date"].min(), "end": df["pub_date"].max()},
        "sentiment_distribution": df["sentiment_class"].value_counts().to_dict(),
        "sentiment_percentages": (df["sentiment_class"].value_counts() / len(df) * 100)
        .round(1)
        .to_dict(),
        "average_score": df["sentiment_score"].mean().round(3),
        "score_stats": {
            "min": df["sentiment_score"].min().round(3),
            "max": df["sentiment_score"].max().round(3),
            "std": df["sentiment_score"].std().round(3),
        },
        "sources": {
            "total_sources": df["source"].nunique(),
            "top_sources": df["source"].value_counts().head(5).to_dict(),
        },
        "word_analysis": {
            "avg_positive_words": df["positive_words_count"].mean().round(1),
            "avg_negative_words": df["negative_words_count"].mean().round(1),
            "total_words_analyzed": df["word_count"].sum()
            if "word_count" in df.columns
            else "N/A",
        },
    }

    most_positive = df.loc[df["sentiment_score"].idxmax()]
    most_negative = df.loc[df["sentiment_score"].idxmin()]

    stats["highlights"] = {
        "most_positive": {
            "title": most_positive["title"],
            "score": most_positive["sentiment_score"].round(3),
            "source": most_positive["source"],
        },
        "most_negative": {
            "title": most_negative["title"],
            "score": most_negative["sentiment_score"].round(3),
            "source": most_negative["source"],
        },
    }

    source_sentiment = (
        df.groupby("source")["sentiment_score"].agg(["mean", "count"]).round(3)
    )
    stats["source_analysis"] = source_sentiment.to_dict()

    return stats
