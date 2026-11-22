WorkOrderType = Literal["PREVENTIVE", "CORRECTIVE", "REHABILITATIVE", "INSPECTION"]
WorkOrderStatus = Literal["OPEN", "IN_PROGRESS", "COMPLETED", "CANCELLED"]
WorkOrderPriority = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


@dataclass
class WorkOrder:
    wo_id: str
    equipment_id: str
    title: str
    wo_type: WorkOrderType
    priority: WorkOrderPriority = "MEDIUM"
    status: WorkOrderStatus = "OPEN"
    assigned_technician: str | None = None
    notes: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str | None = None

    def start(self, technician: str | None = None) -> None:
        if technician:
            self.assigned_technician = technician
        self.status = "IN_PROGRESS"

    def add_note(self, note: str) -> None:
        if note.strip():
            self.notes.append(note.strip())

    def complete(self, closing_note: str | None = None) -> None:
        if closing_note:
            self.add_note(closing_note)
        self.status = "COMPLETED"
        self.completed_at = datetime.now(timezone.utc).isoformat()