from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="ImuMeasurement")


@_attrs_define
class ImuMeasurement:
    """A single IMU sample.

    Used for sequence/SLAM-leaning workflows where camera pose is
    correlated with an IMU stream. ``timestamp_ns`` is the nanosecond
    timestamp on the IMU's clock; ``gyro`` is angular velocity
    (rad/s) and ``accel`` is linear acceleration (m/s²) in the IMU
    body frame.

        Attributes:
            timestamp_ns (int):
            gyro (list[float]):
            accel (list[float]):
    """

    timestamp_ns: int
    gyro: list[float]
    accel: list[float]

    def to_dict(self) -> dict[str, Any]:
        timestamp_ns = self.timestamp_ns

        gyro = []
        for gyro_item_data in self.gyro:
            gyro_item: float
            gyro_item = gyro_item_data
            gyro.append(gyro_item)

        accel = []
        for accel_item_data in self.accel:
            accel_item: float
            accel_item = accel_item_data
            accel.append(accel_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "timestamp_ns": timestamp_ns,
                "gyro": gyro,
                "accel": accel,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp_ns = d.pop("timestamp_ns")

        gyro = []
        _gyro = d.pop("gyro")
        for gyro_item_data in _gyro:

            def _parse_gyro_item(data: object) -> float:
                return cast(float, data)

            gyro_item = _parse_gyro_item(gyro_item_data)

            gyro.append(gyro_item)

        accel = []
        _accel = d.pop("accel")
        for accel_item_data in _accel:

            def _parse_accel_item(data: object) -> float:
                return cast(float, data)

            accel_item = _parse_accel_item(accel_item_data)

            accel.append(accel_item)

        imu_measurement = cls(
            timestamp_ns=timestamp_ns,
            gyro=gyro,
            accel=accel,
        )

        return imu_measurement
