-- Trigger event to occur on update

CREATE TRIGGER update_stock AFTER UPDATE ON users for EACH ROW set @quantity = OLD.quantity - NEW.quantity
