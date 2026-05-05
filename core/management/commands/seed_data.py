from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Skill, Post, UserProfile, Event
import random
from django.db import transaction

class Command(BaseCommand):
    help = 'Seeds the database with a massive diverse SkillMesh population'

    def handle(self, *args, **kwargs):
        self.stdout.write('INITIALIZING TOTAL MESH OVERLOAD...')

        # 1. Define Skills
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

            # 2. The Master Persona List (25+ Nodes)
            personas = [
                # The Cyber Batch
                {'username': 'neon_hacker', 'bio': 'Dark-mode aesthetics and cyber-secure protocols.', 'skills': ['Cybersecurity', 'React', 'Tailwind CSS']},
                {'username': 'bit_architect', 'bio': 'Building low-level foundations.', 'skills': ['Rust', 'Distributed Systems', 'C++']},
                {'username': 'rust_rebel', 'bio': 'Safety and speed master.', 'skills': ['Rust', 'Go', 'Docker']},
                {'username': 'pixel_perfect', 'bio': 'UI precision is my religion.', 'skills': ['UI/UX', 'Tailwind CSS', 'Framer Motion']},
                {'username': 'cloud_weaver', 'bio': 'Orchestrating massive clusters.', 'skills': ['Kubernetes', 'AWS', 'Docker']},
                {'username': 'data_alchemist', 'bio': 'Turning data into gold.', 'skills': ['Machine Learning', 'Python', 'PostgreSQL']},
                {'username': 'solana_surfer', 'bio': 'Riding the blockchain waves.', 'skills': ['Solidity', 'Web3', 'Solana']},
                {'username': 'titan_dev', 'bio': 'Enterprise-scale solutions.', 'skills': ['Go', 'PostgreSQL', 'Kubernetes']},
                {'username': 'orbital_designer', 'bio': 'Interfaces from the year 2050.', 'skills': ['UI/UX', 'Framer Motion', 'React']},
                {'username': 'syntax_samurai', 'bio': 'Clean code, sharp mind.', 'skills': ['TypeScript', 'Next.js', 'Node.js']},
                
                # The Specialist Batch
                {'username': 'alex_dev', 'bio': 'Full-stack engineer specializing in high-performance web apps.', 'skills': ['React', 'Node.js', 'PostgreSQL']},
                {'username': 'sarah_cloud', 'bio': 'Cloud Architect focused on serverless and scalability.', 'skills': ['AWS', 'Docker', 'Kubernetes']},
                {'username': 'mike_ops', 'bio': 'DevOps wizard making deployments smooth as silk.', 'skills': ['Docker', 'Terraform', 'Go']},
                {'username': 'jenny_ai', 'bio': 'AI Researcher exploring the limits of LLMs.', 'skills': ['Python', 'LLMs', 'Machine Learning']},
                {'username': 'ethan_rust', 'bio': 'Low-level enthusiast building safe systems.', 'skills': ['Rust', 'C++', 'Distributed Systems']},
                {'username': 'lila_design', 'bio': 'Visual storyteller and UI/UX artisan.', 'skills': ['UI/UX', 'Framer Motion', 'Tailwind CSS']},
                {'username': 'marcus_backend', 'bio': 'Data engineer optimizing queries for breakfast.', 'skills': ['PostgreSQL', 'Python', 'Go']},
                {'username': 'zoe_frontend', 'bio': 'Creating immersive web experiences.', 'skills': ['TypeScript', 'React', 'Next.js']},
                {'username': 'leo_security', 'bio': 'Defending the mesh from intrusions.', 'skills': ['Cybersecurity', 'Go', 'Docker']},
                {'username': 'maya_web3', 'bio': 'Decentralizing the world, one block at a time.', 'skills': ['Solidity', 'Web3', 'GraphQL']},

                # The Hybrid Batch
                {'username': 'vector_voyager', 'bio': 'Exploring RAG and vector search.', 'skills': ['LLMs', 'RAG', 'PostgreSQL']},
                {'username': 'proto_pilot', 'bio': 'Rapid prototyping specialist.', 'skills': ['React', 'Tailwind CSS', 'Node.js']},
                {'username': 'logic_lord', 'bio': 'Solving algorithmic nightmares.', 'skills': ['C++', 'Python', 'Distributed Systems']},
                {'username': 'mesh_master', 'bio': 'Connecting the world nodes.', 'skills': ['Node.js', 'GraphQL', 'TypeScript']},
                {'username': 'gl_warrior', 'bio': 'Visualizing the matrix in 3D.', 'skills': ['WebGL', 'TypeScript', 'React']}
            ]

            created_count = 0
            for p in personas:
                user, created = User.objects.get_or_create(username=p['username'])
                if created:
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
                    
                    Post.objects.create(
                        user=user,
                        content=f"Initial signal broadcast from {p['username']}. Specializing in {p['skills'][0]}. System online.",
                        post_type='general'
                    )

        self.stdout.write(self.style.SUCCESS(f'TOTAL OVERLOAD COMPLETE: {created_count} NEW NODES INITIALIZED.'))
