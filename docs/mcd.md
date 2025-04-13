```mermaid
    erDiagram
        MEDIA ||--o{ SAISON : "peut avoir"
        SAISON ||--o{ EPISODE : "peut avoir"

        MEDIA {
            int id PK
            string type
            string title
        }
        
        SAISON {
            int id PK
            int media_id FK
            int season_number
        }
        
        EPISODE {
            int id PK
            int saison_id FK
            int episode_number
            boolean watched
            date watch_date
        }
```