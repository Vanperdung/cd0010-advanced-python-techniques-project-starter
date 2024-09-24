"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import operator


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to a reference value. It
    essentially functions as a callable predicate for whether a `CloseApproach`
    object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).

    Concrete subclasses can override the `get` classmethod to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """
    
    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from an binary predicate and a reference value.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must override this method to get an attribute of
        interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        """Return a string representation of the object.

        This method returns a string that shows the class name, the operator used in the object,
        and the value. It's useful for debugging and provides a detailed representation of the object.

        :return: A string representation of the object, including the operator and value.
        """
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"

class DateFilter(AttributeFilter):
    """A child class for date-filters.

    It only contains one class method for getting the value.
    """
    
    @classmethod
    def get(cls, approach):
        """Get the date of the close approach.

        This class method extracts the `date` from the `time` attribute of the `approach` object,
        which is a `CloseApproach` instance. The `time` attribute is a `datetime`, and this method
        returns the `date` portion of that `datetime`.

        :param approach: A `CloseApproach` object from which to extract the date.
        :return: A `date` object representing the date of the close approach.
        """
        return approach.time.date()

class DistanceFilter(AttributeFilter):
    """A filter for the distance of a close approach.

    This filter checks the `distance` attribute of a `CloseApproach` object.
    It is used to filter close approaches based on the distance from Earth, expressed in astronomical units (AU).
    """
    
    @classmethod
    def get(cls, approach):
        """Get the distance of the close approach.

        This method extracts the `distance` attribute from the `approach` object,
        which represents the distance in astronomical units (AU) of the close approach.

        :param approach: A `CloseApproach` object from which to extract the distance.
        :return: A float representing the distance in AU.
        """
        return approach.distance

class VelocityFilter(AttributeFilter):
    """A filter for the velocity of a close approach.

    This filter checks the `velocity` attribute of a `CloseApproach` object.
    It is used to filter close approaches based on the velocity of the NEO during the approach, expressed in kilometers per second.
    """
    
    @classmethod
    def get(cls, approach):
        """Get the velocity of the close approach.

        This method extracts the `velocity` attribute from the `approach` object,
        which represents the velocity of the object during the close approach in kilometers per second.

        :param approach: A `CloseApproach` object from which to extract the velocity.
        :return: A float representing the velocity in km/s.
        """
        return approach.velocity

class DiameterFilter(AttributeFilter):
    """A filter for the diameter of a near-Earth object (NEO).

    This filter checks the `diameter` attribute of the `neo` associated with a `CloseApproach` object.
    It is used to filter close approaches based on the NEO's diameter, expressed in kilometers.
    """
    
    @classmethod
    def get(cls, approach):
        """Get the diameter of the near-Earth object (NEO).

        This method extracts the `diameter` attribute from the `neo` associated
        with the `approach` object. The `diameter` represents the diameter of
        the NEO in kilometers.

        :param approach: A `CloseApproach` object from which to extract the NEO's diameter.
        :return: A float representing the diameter in kilometers, or `None` if unknown.
        """
        return approach.neo.diameter

class HazardousFilter(AttributeFilter):
    """A filter for the hazardous status of a near-Earth object (NEO).

    This filter checks the `hazardous` attribute of the `neo` associated with a `CloseApproach` object.
    It is used to filter close approaches based on whether the NEO is potentially hazardous.
    """
    
    @classmethod
    def get(cls, approach):
        """Check if the near-Earth object (NEO) is potentially hazardous.

        This method extracts the `hazardous` attribute from the `neo` associated
        with the `approach` object. It returns a boolean indicating whether the
        NEO is considered potentially hazardous.

        :param approach: A `CloseApproach` object from which to extract the hazardous status.
        :return: A boolean indicating if the NEO is hazardous (`True` or `False`).
        """
        return approach.neo.hazardous

def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from the
    user's options at the command line. Each one corresponds to a different type
    of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that occurred
    on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of `NEODatabase`
    because the main module directly passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """    
    command_filters = []

    if date is not None:
        command_filters.append(DateFilter(operator.eq, date))
    if start_date is not None:
        command_filters.append(DateFilter(operator.ge, start_date))
    if end_date is not None:
        command_filters.append(DateFilter(operator.le, end_date))
    if distance_min is not None:
        command_filters.append(DistanceFilter(operator.ge, distance_min))
    if distance_max is not None:
        command_filters.append(DistanceFilter(operator.le, distance_max))
    if velocity_min is not None:
        command_filters.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max is not None:
        command_filters.append(VelocityFilter(operator.le, velocity_max))
    if diameter_min is not None:
        command_filters.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max is not None:
        command_filters.append(DiameterFilter(operator.le, diameter_max))    
    if hazardous is not None:
        command_filters.append(HazardousFilter(operator.eq, hazardous))

    return command_filters 

def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if n is None or n == 0:
        yield from iterator
    else:
        for i, value in enumerate(iterator):
            if i >= n:
                break
            yield value