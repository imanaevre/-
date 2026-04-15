import pandas as pd

class AdvancedStudentAnalytics:

    def __init__(self, df):
        self.df = df
        self._prepare_data()

    def _prepare_data(self):
        self.df['project_score'] = self.df['project_score'].fillna(
            self.df['project_score'].median()
        )

        self.df['average_grade'] = self.df[['math', 'physics', 'cs']].mean(axis=1)

        def performance(avg):
            if avg >= 85:
                return 'high'
            elif avg >= 70:
                return 'medium'
            else:
                return 'low'

        self.df['performance_level'] = self.df['average_grade'].apply(performance)

        def risk(row):
            if row['attendance'] < 60 or row['average_grade'] < 65:
                return 'high risk'
            elif 60 <= row['attendance'] <= 75:
                return 'medium risk'
            else:
                return 'low risk'

        self.df['risk_level'] = self.df.apply(risk, axis=1)

    # 1
    def top_students(self, n):
        return self.df.sort_values('average_grade', ascending=False).head(n)

    # 2
    def group_stats(self):
        return self.df.groupby('group').agg({
            'average_grade': 'mean',
            'attendance': 'mean',
            'name': 'count'
        }).rename(columns={'name': 'student_count'})

    # 3
    def at_risk_students(self):
        return self.df[self.df['risk_level'] == 'high risk']

    # 4
    def scholarship_analysis(self):
        return self.df.groupby('scholarship').agg({
            'average_grade': 'mean',
            'attendance': 'mean'
        })

    # 5
    def city_performance(self):
        city_avg = self.df.groupby('city')['average_grade'].mean()
        return {
            'best_city': city_avg.idxmax(),
            'worst_city': city_avg.idxmin()
        }

    # 6
    def hidden_top_students(self):
        return self.df[
            (self.df['average_grade'] > 85) &
            (self.df['scholarship'] == False)
        ]

    # 7
    def lazy_geniuses(self):
        return self.df[
            (self.df['average_grade'] > 85) &
            (self.df['attendance'] < 60)
        ]

    # 3 (main)
    def full_analysis(self):
        return {
            'top_3_students': self.top_students(3),
            'group_stats': self.group_stats(),
            'high_risk_count': len(self.at_risk_students()),
            'hidden_top_count': len(self.hidden_top_students()),
            'lazy_genius_count': len(self.lazy_geniuses()),
            'city_performance': self.city_performance(),
            'scholarship_analysis': self.scholarship_analysis()
        }

df = pd.read_csv('students_extended.csv')

analytics = AdvancedStudentAnalytics(df)

print(analytics.top_students(3))
print(analytics.group_stats())
print(analytics.full_analysis())
