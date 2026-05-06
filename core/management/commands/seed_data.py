from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Skill, Post, UserProfile, Event
import random
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with a massive diverse SkillMesh population and historical events'

    def handle(self, *args, **kwargs):
        self.stdout.write('INITIALIZING TIME-TRAVEL MESH OVERLOAD...')

        now = timezone.now()
        day_minus_2 = now - timedelta(days=2)
        day_minus_1 = now - timedelta(days=1)

        protocols = [
            'Rust', 'Solidity', 'React', 'TypeScript', 'Python', 
            'UI/UX', 'Distributed Systems', 'PostgreSQL', 'Docker',
            'LLMs', 'Tailwind CSS', 'Framer Motion', 'Web3', 'Cybersecurity',
            'Go', 'Kubernetes', 'Machine Learning', 'Swift', 'C++', 'Node.js',
            'AWS', 'Terraform', 'GraphQL', 'Next.js', 'Solana', 'WebGL', 'RAG'
        ]
        
        with transaction.atomic():
            for p in protocols:
                Skill.objects.get_or_create(name=p)

            personas = [
                # Day -2: Early Adopters
                {'username': 'neon_hacker', 'bio': 'Dark-mode aesthetics and cyber-secure protocols.', 'skills': ['Cybersecurity', 'React'], 'day': day_minus_2},
                {'username': 'bit_architect', 'bio': 'Building low-level foundations.', 'skills': ['Rust', 'Distributed Systems'], 'day': day_minus_2},
                {'username': 'rust_rebel', 'bio': 'Safety and speed master.', 'skills': ['Rust', 'Go'], 'day': day_minus_2},
                {'username': 'pixel_perfect', 'bio': 'UI precision is my religion.', 'skills': ['UI/UX', 'Tailwind CSS'], 'day': day_minus_2},
                {'username': 'cloud_weaver', 'bio': 'Orchestrating massive clusters.', 'skills': ['Kubernetes', 'AWS'], 'day': day_minus_2},
                
                # Day -1: The Growth Phase
                {'username': 'data_alchemist', 'bio': 'Turning data into gold.', 'skills': ['Machine Learning', 'Python'], 'day': day_minus_1},
                {'username': 'solana_surfer', 'bio': 'Riding the blockchain waves.', 'skills': ['Solidity', 'Web3'], 'day': day_minus_1},
                {'username': 'titan_dev', 'bio': 'Enterprise-scale solutions.', 'skills': ['Go', 'PostgreSQL'], 'day': day_minus_1},
                {'username': 'orbital_designer', 'bio': 'Interfaces from the year 2050.', 'skills': ['UI/UX', 'Framer Motion'], 'day': day_minus_1},
                {'username': 'syntax_samurai', 'bio': 'Clean code, sharp mind.', 'skills': ['TypeScript', 'Next.js'], 'day': day_minus_1},
                
                # Today: Current Wave
                {'username': 'alex_dev', 'bio': 'Full-stack engineer.', 'skills': ['React', 'Node.js'], 'day': now},
                {'username': 'sarah_cloud', 'bio': 'Cloud Architect.', 'skills': ['AWS', 'Docker'], 'day': now},
                {'username': 'jenny_ai', 'bio': 'AI Researcher.', 'skills': ['Python', 'LLMs'], 'day': now},
                {'username': 'vector_voyager', 'bio': 'Exploring RAG.', 'skills': ['LLMs', 'RAG'], 'day': now},
                {'username': 'gl_warrior', 'bio': '3D matrix visualization.', 'skills': ['WebGL', 'TypeScript'], 'day': now}
            ]

            created_count = 0
            for p in personas:
                user, created = User.objects.get_or_create(username=p['username'])
                if created:
                    user.date_joined = p['day']
                    user.email = f"{p['username']}@mesh.com"
                    user.set_password('skillmesh123')
                    user.save()
                    created_count += 1
                
                    profile, _ = UserProfile.objects.get_or_create(user=user)
                    profile.bio = p['bio']
                    profile.save()
                    
                    for s_name in p['skills']:
                        skill, _ = Skill.objects.get_or_create(name=s_name)
                        profile.skills.add(skill)
                    
                    # Log the Identity Creation with the specific day
                    Event.objects.create(
                        event_type='IdentityCreated',
                        timestamp=p['day'],
                        processing_time=random.uniform(100, 250),
                        status='success'
                    )

                    # Create some historical posts
                    post_day = p['day'] + timedelta(hours=random.randint(1, 5))
                    Post.objects.create(
                        user=user,
                        content=f"Node {p['username']} initialized. Protocol: {p['skills'][0]}. Broadcast timestamp: {post_day}.",
                        post_type='general',
                        created_at=post_day
                    )
                    
                    # Manually log the historical post event
                    Event.objects.create(
                        event_type='PostCreated',
                        timestamp=post_day,
                        processing_time=random.uniform(50, 100),
                        status='success'
                    )

                    # Simulate a profile update later for some
                    if random.random() > 0.5:
                        update_day = post_day + timedelta(hours=random.randint(2, 10))
                        Event.objects.create(
                            event_type='ProfileUpdated',
                            timestamp=update_day,
                            processing_time=random.uniform(30, 60),
                            status='success'
                        )

        self.stdout.write(self.style.SUCCESS(f'TIME-TRAVEL COMPLETE: {created_count} HISTORICAL NODES INITIALIZED.'))
