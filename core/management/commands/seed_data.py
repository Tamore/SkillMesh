from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Skill, Post, UserProfile, Event
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the database with a massive diverse SkillMesh population'

    def handle(self, *args, **kwargs):
        self.stdout.write('INITIALIZING MASS POPULATION SEQUENCE...')

        # 1. Define Skills
        protocols = [
            'Rust', 'Solidity', 'React', 'TypeScript', 'Python', 
            'UI/UX', 'Distributed Systems', 'PostgreSQL', 'Docker',
            'LLMs', 'Tailwind CSS', 'Framer Motion', 'Web3', 'Cybersecurity',
            'Go', 'Kubernetes', 'Machine Learning', 'Swift', 'C++', 'Node.js',
            'AWS', 'Terraform', 'GraphQL', 'Next.js', 'Solana'
        ]
        
        for p in protocols:
            Skill.objects.get_or_create(name=p)

        # 2. Define Personas (15 New Nodes)
        personas = [
            {'username': 'neon_hacker', 'bio': 'Specializing in dark-mode aesthetics and cyber-secure protocols.', 'skills': ['Cybersecurity', 'React', 'Tailwind CSS']},
            {'username': 'bit_architect', 'bio': 'Building the foundations of the next-gen web. Low-level lover.', 'skills': ['Rust', 'Distributed Systems', 'C++']},
            {'username': 'rust_rebel', 'bio': 'Safety and speed. Rust is the only way forward.', 'skills': ['Rust', 'Go', 'Docker']},
            {'username': 'pixel_perfect', 'bio': 'If it is one pixel off, it is broken. UI precision is my religion.', 'skills': ['UI/UX', 'Tailwind CSS', 'Framer Motion']},
            {'username': 'cloud_weaver', 'bio': 'Orchestrating massive clusters. Kubernetes is my playground.', 'skills': ['Kubernetes', 'AWS', 'Docker']},
            {'username': 'data_alchemist', 'bio': 'Turning raw data into gold using Python and ML.', 'skills': ['Machine Learning', 'Python', 'PostgreSQL']},
            {'username': 'solana_surfer', 'bio': 'Riding the waves of high-speed blockchain transactions.', 'skills': ['Solidity', 'Web3', 'Solana']},
            {'username': 'titan_dev', 'bio': 'Enterprise-scale solutions for massive problems.', 'skills': ['Go', 'PostgreSQL', 'Kubernetes']},
            {'username': 'orbital_designer', 'bio': 'Creating interfaces that feel like they are from 2050.', 'skills': ['UI/UX', 'Framer Motion', 'React']},
            {'username': 'syntax_samurai', 'bio': 'Clean code, sharp mind. TypeScript master.', 'skills': ['TypeScript', 'Next.js', 'Node.js']},
            {'username': 'proto_pilot', 'bio': 'Rapid prototyping and high-speed delivery.', 'skills': ['React', 'Tailwind CSS', 'Node.js']},
            {'username': 'logic_lord', 'bio': 'Solving the hardest algorithmic challenges.', 'skills': ['C++', 'Python', 'Distributed Systems']},
            {'username': 'vector_voyager', 'bio': 'Exploring the world of vector databases and RAG.', 'skills': ['LLMs', 'Python', 'PostgreSQL']},
            {'username': 'cyber_sage', 'bio': 'Wisdom in the world of encryption and security.', 'skills': ['Cybersecurity', 'Go', 'Rust']},
            {'username': 'mesh_master', 'bio': 'Connecting the nodes of the world.', 'skills': ['Node.js', 'GraphQL', 'TypeScript']}
        ]

        created_count = 0
        for p in personas:
            # Use only username for get_or_create to avoid email collisions
            user, created = User.objects.get_or_create(username=p['username'])
            if created:
                user.email = f"{p['username']}@mesh.com"
                user.set_password('skillmesh123')
                user.save()
                created_count += 1
            
                # Update Profile
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profile.bio = p['bio']
                profile.save()
                
                # Add Skills
                for s_name in p['skills']:
                    skill = Skill.objects.get(name=s_name)
                    profile.skills.add(skill)
                
                # Create a Post for each new user
                Post.objects.create(
                    user=user,
                    content=f"Greetings Mesh! I am {p['username']}, focusing on {p['skills'][0]}. Excited to connect.",
                    post_type='general'
                )

                # LOG EVENT so dashboard updates
                Event.objects.create(
                    event_type='IdentityCreated',
                    status='success',
                    processing_time=random.randint(50, 200)
                )

        self.stdout.write(self.style.SUCCESS(f'MASS POPULATION COMPLETE: {created_count} NEW NODES INITIALIZED.'))
