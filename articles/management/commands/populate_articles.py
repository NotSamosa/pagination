from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from articles.models import Article

class Command(BaseCommand):
    help = 'Populates the database with sample articles for pagination testing'

    def handle(self, *args, **options):
        titles = [
            'Understanding Django REST Framework Pagination',
            'Deep Dive into Database Indexing with PostgreSQL',
            'Building Scalable APIs with Python and Django',
            'Mastering QuerySet Optimization Techniques',
            'Clean Architecture Principles in Python Web Apps',
            'Asynchronous Programming with Asyncio and Celery',
            'Designing RESTful Services: Best Practices and Pitfalls',
            'Demystifying Python Descriptors and Metaclasses',
            'Effective Unit Testing Strategies for Django APIs',
            'Containerizing Django Applications with Docker and Compose',
            'Caching Strategies Using Redis in Modern Web Systems',
            'Securing Web Applications with OAuth2 and JWT',
            'Continuous Integration and Continuous Deployment Pipelines',
            'Microservices vs Modular Monolith: Practical Tradeoffs',
            'Event-Driven Architectures with Kafka and RabbitMQ',
            'Database Sharding and Replication Patterns Explained',
            'Frontend Pagination: Infinite Scroll vs Numbered Pages',
            'Profiling and Benchmarking High-Throughput APIs',
            'Handling Concurrency with Optimistic and Pessimistic Locking',
            'Effective Monitoring and Observability with Prometheus'
        ]

        authors = [
            'Sarah Chen',
            'David Miller',
            'Alex Rivera',
            'Elena Rostova',
            'Marcus Vance',
            'Priya Patel',
            'Liam O\'Connor',
            'Kenji Sato'
        ]

        Article.objects.all().delete()

        now = timezone.now()
        articles_to_create = []

        total_count = 60
        for i in range(1, total_count + 1):
            title_base = random.choice(titles)
            title = f'{title_base} - Part {i}'
            content = (
                f'This article explores technical details, benchmarks, and real-world architectures '
                f'regarding {title_base.lower()}. We examine edge cases, scalability profiles, and '
                f'practical implementations across production environments in chapter {i}.'
            )
            author = random.choice(authors)
            is_published = (i <= 52)
            created_at = now - timedelta(days=total_count - i, hours=i % 24, minutes=i % 60)

            article = Article(
                title=title,
                content=content,
                author=author,
                is_published=is_published
            )
            articles_to_create.append((article, created_at))

        for article, created_at in articles_to_create:
            article.save()
            Article.objects.filter(id=article.id).update(created_at=created_at)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {total_count} articles ({52} published, {8} drafts).')
        )
