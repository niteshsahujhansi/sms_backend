# Future Features - Schedule Module

## Advanced/Enterprise Fields (Planned for Future Implementation)

These fields were removed from the current Schedule model but are planned for future implementation:

### Notes and Event Management
- `notes` (Text, nullable=True) - Additional notes for the schedule entry
- `event_type` (EventTypeEnum, nullable=True) - Type of event (Regular, Exam, Assembly, Holiday, Special)

### Advanced Scheduling
- `batch_id` (UUID, nullable=True) - For batch-based scheduling
- `week_number` (Integer, nullable=True) - For weekly rotation schedules
- `term` (String, nullable=True) - Academic term (e.g., "First Term", "Second Term")
- `group_id` (UUID, nullable=True) - For group-based scheduling

### UI/UX Enhancements
- `color` (String, nullable=True) - Color coding for different subjects or event types

## Implementation Priority
1. Core scheduling functionality (current implementation)
2. Notes and event types
3. Advanced scheduling features
4. UI/UX enhancements

## Migration Notes
When implementing these features, create a new database migration to add the columns. 