import unittest
from utils.transformation import JsonTransformation


class TestJsonTransformation(unittest.TestCase):

    def setUp(self):
        json_data = [
            {'title': 'The New Legend of Shaolin',
             'countries': ['Hong Kong'],
             'fullplot': 'A young father and his infant son are beset by forces of evil and corruption. They wander China, upholding their sense of honor and protecting the weak. When they are forced into combat, spectacular and hilarious fast-motion kung fu sequences follow. In the end, they must call on all of their abilities in a battle royale, to attempt to vanquish a supernatural man-monster or die trying.',
             '@search.score': 0.8649507,
             '@search.reranker_score': None,
             '@search.highlights': None,
             '@search.captions': None
             },
            {'title': 'The Prodigal Son',
             'countries': ['Hong Kong'],
             'fullplot': "A rich man's son (Yuen Biao) believes himself to be the best kung fu fighter in Canton. Unfortunately, his father, anxious for his son's safety, bribes all his opponents to lose. After a humiliating defeat at the hands of an actor in a traveling theatre company, the son resolves to find a better teacher. Furious kung fu battles and slapstick comedy.",
             '@search.score': 0.86450726,
             '@search.reranker_score': None,
             '@search.highlights': None,
             '@search.captions': None
             },
            {'title': 'The Enforcer',
             'countries': ['Hong Kong'],
             'fullplot': 'Kung Wei (Jet Li), a undercover Chinese cop sent to track down a notorious criminal Po Kwong (Yu Rongguang) in Hong Kong. There, he ultimately teams with his son Johnny Kung (Xie Miao) and a another cop Anna Fong (Anita Mui), the both together are an incredible Kung Fu master-in-the-making. Together, they lay down the law in the final fight on Po.',
             '@search.score': 0.86292636,
             '@search.reranker_score': None,
             '@search.highlights': None,
             '@search.captions': None
             }
        ]
        self.tran = JsonTransformation(json_data)

    def test_filter_fields(self):
        fields_to_remove = ["@search.score", "@search.reranker_score", "@search.highlights", "@search.captions"]
        data_transformed = self.tran.filter_fields(fields_to_remove)
        data_expected = [
            {'title': 'The New Legend of Shaolin',
             'countries': ['Hong Kong'],
             'fullplot': 'A young father and his infant son are beset by forces of evil and corruption. They wander China, upholding their sense of honor and protecting the weak. When they are forced into combat, spectacular and hilarious fast-motion kung fu sequences follow. In the end, they must call on all of their abilities in a battle royale, to attempt to vanquish a supernatural man-monster or die trying.'
             },
            {'title': 'The Prodigal Son',
             'countries': ['Hong Kong'],
             'fullplot': "A rich man's son (Yuen Biao) believes himself to be the best kung fu fighter in Canton. Unfortunately, his father, anxious for his son's safety, bribes all his opponents to lose. After a humiliating defeat at the hands of an actor in a traveling theatre company, the son resolves to find a better teacher. Furious kung fu battles and slapstick comedy."
             },
            {'title': 'The Enforcer',
             'countries': ['Hong Kong'],
             'fullplot': 'Kung Wei (Jet Li), a undercover Chinese cop sent to track down a notorious criminal Po Kwong (Yu Rongguang) in Hong Kong. There, he ultimately teams with his son Johnny Kung (Xie Miao) and a another cop Anna Fong (Anita Mui), the both together are an incredible Kung Fu master-in-the-making. Together, they lay down the law in the final fight on Po.'
             }
        ]
        self.assertEqual(data_transformed, data_expected)


if __name__ == "__main__":
    unittest.main()
