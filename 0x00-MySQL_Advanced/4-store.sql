-- Trigger event to occur on update

CREATE root@'localhost' TRIGGER update_stock AFTER UPDATE ON users for EACH ROW set @quantity = OLD.quantity - NEW.quantity
